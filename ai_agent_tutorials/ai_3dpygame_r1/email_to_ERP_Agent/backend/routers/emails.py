"""
API routes for email processing.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from ..auth.oauth import get_current_user
from ..email_processor.email_client import EmailProcessor, GmailClient
from ..models.email import EmailResponse
from ..models.sku import SKUResponse

router = APIRouter(
    prefix="/api/emails",
    tags=["emails"]
)


@router.get("/", response_model=List[EmailResponse])
async def get_emails(
    query: Optional[str] = Query(None, description="Gmail search query"),
    max_results: int = Query(10, description="Maximum number of emails to fetch"),
    current_user = Depends(get_current_user)
):
    """
    Get emails from Gmail.
    """
    try:
        # In a real implementation, we would get these from user settings
        token_path = f"tokens/{current_user.id}/gmail_token.json"
        credentials_path = "credentials/gmail_credentials.json"
        
        # Create Gmail client
        gmail_client = GmailClient(token_path, credentials_path)
        
        # Fetch emails
        gmail_messages = gmail_client.fetch_emails(query, max_results)
        
        # Parse emails
        emails = [gmail_client.parse_email(msg) for msg in gmail_messages]
        
        # Convert to response model
        email_responses = [
            EmailResponse(
                id=email.id,
                thread_id=email.thread_id,
                subject=email.subject,
                from_email=email.from_email,
                date=email.date.isoformat(),
                body_preview=email.body[:200] + "..." if len(email.body) > 200 else email.body,
                attachment_count=len(email.attachments),
                labels=email.labels,
                processed=email.processed
            ) for email in emails
        ]
        
        return email_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(
    email_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get email by ID.
    """
    try:
        # In a real implementation, we would get these from user settings
        token_path = f"tokens/{current_user.id}/gmail_token.json"
        credentials_path = "credentials/gmail_credentials.json"
        
        # Create Gmail client
        gmail_client = GmailClient(token_path, credentials_path)
        
        # Authenticate
        if not gmail_client.authenticate():
            raise HTTPException(status_code=401, detail="Failed to authenticate with Gmail")
        
        # Get message
        message = gmail_client.service.users().messages().get(
            userId='me', 
            id=email_id,
            format='full'
        ).execute()
        
        # Parse email
        email = gmail_client.parse_email(message)
        
        # Convert to response model
        email_response = EmailResponse(
            id=email.id,
            thread_id=email.thread_id,
            subject=email.subject,
            from_email=email.from_email,
            date=email.date.isoformat(),
            body_preview=email.body[:200] + "..." if len(email.body) > 200 else email.body,
            attachment_count=len(email.attachments),
            labels=email.labels,
            processed=email.processed
        )
        
        return email_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{email_id}/skus", response_model=List[SKUResponse])
async def get_email_skus(
    email_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get SKUs from email.
    """
    try:
        # In a real implementation, we would get these from user settings
        token_path = f"tokens/{current_user.id}/gmail_token.json"
        credentials_path = "credentials/gmail_credentials.json"
        
        # Create Gmail client
        gmail_client = GmailClient(token_path, credentials_path)
        
        # Create email processor
        email_processor = EmailProcessor(gmail_client)
        
        # Authenticate
        if not gmail_client.authenticate():
            raise HTTPException(status_code=401, detail="Failed to authenticate with Gmail")
        
        # Get message
        message = gmail_client.service.users().messages().get(
            userId='me', 
            id=email_id,
            format='full'
        ).execute()
        
        # Parse email
        email = gmail_client.parse_email(message)
        
        # Extract SKUs
        skus = email_processor.extract_skus(email)
        
        # Set source email ID
        for sku in skus:
            sku.source_email_id = email.id
        
        # Convert to response model
        sku_responses = [
            SKUResponse(
                sku_code=sku.sku_code,
                quantity=sku.quantity,
                source_email_id=sku.source_email_id,
                validated=sku.validated,
                erp_entry_id=sku.erp_entry_id
            ) for sku in skus
        ]
        
        return sku_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{email_id}/process", response_model=List[SKUResponse])
async def process_email(
    email_id: str,
    current_user = Depends(get_current_user)
):
    """
    Process email and extract SKUs.
    """
    try:
        # In a real implementation, we would get these from user settings
        token_path = f"tokens/{current_user.id}/gmail_token.json"
        credentials_path = "credentials/gmail_credentials.json"
        
        # Create Gmail client
        gmail_client = GmailClient(token_path, credentials_path)
        
        # Create email processor
        email_processor = EmailProcessor(gmail_client)
        
        # Authenticate
        if not gmail_client.authenticate():
            raise HTTPException(status_code=401, detail="Failed to authenticate with Gmail")
        
        # Get message
        message = gmail_client.service.users().messages().get(
            userId='me', 
            id=email_id,
            format='full'
        ).execute()
        
        # Parse email
        email = gmail_client.parse_email(message)
        
        # Extract SKUs
        skus = email_processor.extract_skus(email)
        
        # Set source email ID
        for sku in skus:
            sku.source_email_id = email.id
        
        # Mark email as processed
        if skus:
            email.processed = True
            gmail_client.mark_as_read(email.id)
        
        # Convert to response model
        sku_responses = [
            SKUResponse(
                sku_code=sku.sku_code,
                quantity=sku.quantity,
                source_email_id=sku.source_email_id,
                validated=sku.validated,
                erp_entry_id=sku.erp_entry_id
            ) for sku in skus
        ]
        
        return sku_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
