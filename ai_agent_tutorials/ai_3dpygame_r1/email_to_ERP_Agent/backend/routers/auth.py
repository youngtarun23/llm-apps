"""
API routes for authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any, Optional
import json
import os
from datetime import datetime, timedelta

from ..auth.oauth import create_access_token, get_current_user, oauth2_scheme
from ..models.user import User, UserCreate, UserResponse, TokenResponse

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate = Body(...)
):
    """
    Register a new user.
    """
    try:
        # In a real implementation, we would store this in a database
        # For now, we'll just return a mock response
        user = User(
            id="user_" + datetime.now().strftime("%Y%m%d%H%M%S"),
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            company=user_data.company,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create token directory
        os.makedirs(f"tokens/{user.id}", exist_ok=True)
        
        # Convert to response model
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company=user.company,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
        
        return user_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Get access token.
    """
    try:
        # In a real implementation, we would validate credentials against a database
        # For now, we'll just create a token for any username/password
        
        # Create mock user
        user = User(
            id="user_" + datetime.now().strftime("%Y%m%d%H%M%S"),
            email=form_data.username,
            first_name="John",
            last_name="Doe",
            company="Acme Inc.",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(minutes=30)
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user.
    """
    try:
        # Convert to response model
        user_response = UserResponse(
            id=current_user.id,
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            company=current_user.company,
            created_at=current_user.created_at.isoformat(),
            updated_at=current_user.updated_at.isoformat()
        )
        
        return user_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/google/authorize")
async def google_authorize(
    request: Request
):
    """
    Authorize with Google.
    """
    try:
        # In a real implementation, we would redirect to Google's OAuth page
        # For now, we'll just return a mock response
        return {
            "url": "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=https://www.googleapis.com/auth/gmail.readonly&access_type=offline"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/google/callback")
async def google_callback(
    code: str,
    state: Optional[str] = None
):
    """
    Google OAuth callback.
    """
    try:
        # In a real implementation, we would exchange the code for tokens
        # For now, we'll just return a mock response
        return {
            "message": "Google authentication successful. You can close this window."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
