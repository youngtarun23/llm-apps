from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import secrets
import logging
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

from database import get_db
from .oauth import create_access_token, get_current_user, User
from .models import User as UserModel, OAuthState, OAuthToken, Company
from .utils import get_password_hash, verify_password

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@router.post("/token", response_model=Dict[str, Any])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    """
    # Find user by email
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "company_id": user.company_id
        }
    }

@router.get("/google/auth")
async def google_auth(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Start Google OAuth flow
    """
    # Create OAuth flow
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [GOOGLE_REDIRECT_URI]
            }
        },
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    
    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in database
    oauth_state = OAuthState(
        state=state,
        provider="gmail",
        redirect_uri=str(request.url_for("google_callback")),
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(oauth_state)
    db.commit()
    
    # Get authorization URL
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=state,
        prompt="consent"
    )
    
    return {"authorization_url": authorization_url}

@router.get("/google/callback")
async def google_callback(
    request: Request,
    state: str,
    code: Optional[str] = None,
    error: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback
    """
    # Check for error
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {error}"
        )
    
    # Verify state parameter
    oauth_state = db.query(OAuthState).filter(OAuthState.state == state).first()
    if not oauth_state or oauth_state.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired state parameter"
        )
    
    # Create OAuth flow
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [GOOGLE_REDIRECT_URI]
            }
        },
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
        state=state
    )
    
    # Exchange authorization code for tokens
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Get user info from Google
    user_info_service = build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    
    # Find or create user
    user = db.query(UserModel).filter(UserModel.email == user_info["email"]).first()
    
    if not user:
        # Extract domain from email
        domain = user_info["email"].split("@")[1]
        
        # Find or create company
        company = db.query(Company).filter(Company.domain == domain).first()
        if not company:
            company = Company(
                name=domain.split(".")[0].capitalize(),
                domain=domain
            )
            db.add(company)
            db.flush()
        
        # Create new user
        user = UserModel(
            email=user_info["email"],
            full_name=user_info.get("name", ""),
            company_id=company.id,
            # Set a random password for OAuth users
            hashed_password=get_password_hash(secrets.token_urlsafe(16))
        )
        db.add(user)
        db.flush()
    
    # Store OAuth tokens
    oauth_token = db.query(OAuthToken).filter(
        OAuthToken.user_id == user.id,
        OAuthToken.provider == "gmail"
    ).first()
    
    if oauth_token:
        # Update existing token
        oauth_token.access_token = credentials.token
        oauth_token.refresh_token = credentials.refresh_token or oauth_token.refresh_token
        oauth_token.token_type = credentials.token_type
        oauth_token.expires_at = datetime.fromtimestamp(credentials.expiry.timestamp())
        oauth_token.scope = " ".join(credentials.scopes)
    else:
        # Create new token
        oauth_token = OAuthToken(
            user_id=user.id,
            provider="gmail",
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_type=credentials.token_type,
            expires_at=datetime.fromtimestamp(credentials.expiry.timestamp()),
            scope=" ".join(credentials.scopes)
        )
        db.add(oauth_token)
    
    # Commit changes
    db.commit()
    
    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Redirect to frontend with token
    redirect_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/auth/callback?token={access_token}"
    return {"redirect_url": redirect_url}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user
