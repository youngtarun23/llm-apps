from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from database import get_db
from auth.oauth import get_current_user, User
from .models import (
    EmailConfig, EmailMessage, EmailProcessingResult,
    EmailConfigCreate, EmailConfigUpdate, EmailConfigResponse, EmailMessageResponse
)
from .processor import EmailProcessor

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/configs", response_model=EmailConfigResponse)
async def create_email_config(
    config: EmailConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new email configuration
    """
    # Check if config already exists for this email
    existing_config = db.query(EmailConfig).filter(
        EmailConfig.user_id == current_user.id,
        EmailConfig.email_address == config.email_address
    ).first()
    
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email configuration already exists for this email address"
        )
    
    # Create new config
    db_config = EmailConfig(
        user_id=current_user.id,
        company_id=current_user.company_id,
        email_address=config.email_address,
        labels_to_monitor=config.labels_to_monitor,
        polling_interval=config.polling_interval
    )
    
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    return db_config

@router.get("/configs", response_model=List[EmailConfigResponse])
async def get_email_configs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all email configurations for the current user
    """
    configs = db.query(EmailConfig).filter(
        EmailConfig.user_id == current_user.id
    ).all()
    
    return configs

@router.get("/configs/{config_id}", response_model=EmailConfigResponse)
async def get_email_config(
    config_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific email configuration
    """
    config = db.query(EmailConfig).filter(
        EmailConfig.id == config_id,
        EmailConfig.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    
    return config

@router.put("/configs/{config_id}", response_model=EmailConfigResponse)
async def update_email_config(
    config_id: int,
    config_update: EmailConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an email configuration
    """
    config = db.query(EmailConfig).filter(
        EmailConfig.id == config_id,
        EmailConfig.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    
    # Update fields
    if config_update.labels_to_monitor is not None:
        config.labels_to_monitor = config_update.labels_to_monitor
    
    if config_update.polling_interval is not None:
        config.polling_interval = config_update.polling_interval
    
    if config_update.is_active is not None:
        config.is_active = config_update.is_active
    
    db.commit()
    db.refresh(config)
    
    return config

@router.delete("/configs/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email_config(
    config_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an email configuration
    """
    config = db.query(EmailConfig).filter(
        EmailConfig.id == config_id,
        EmailConfig.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    
    db.delete(config)
    db.commit()
    
    return None

@router.post("/process", status_code=status.HTTP_202_ACCEPTED)
async def process_emails(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger email processing for all active configurations
    """
    # Get all active configs for the user
    configs = db.query(EmailConfig).filter(
        EmailConfig.user_id == current_user.id,
        EmailConfig.is_active == True
    ).all()
    
    if not configs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active email configurations found"
        )
    
    # Process emails in background
    for config in configs:
        processor = EmailProcessor(db, config.id)
        background_tasks.add_task(processor.process_emails)
    
    return {"message": "Email processing started"}

@router.get("/messages", response_model=List[EmailMessageResponse])
async def get_email_messages(
    config_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get processed email messages
    """
    # Base query
    query = db.query(EmailMessage).join(
        EmailConfig, EmailMessage.config_id == EmailConfig.id
    ).filter(
        EmailConfig.user_id == current_user.id
    )
    
    # Apply filters
    if config_id:
        query = query.filter(EmailMessage.config_id == config_id)
    
    if status:
        query = query.filter(EmailMessage.processing_status == status)
    
    # Apply pagination
    messages = query.order_by(EmailMessage.received_at.desc()).offset(offset).limit(limit).all()
    
    return messages

@router.get("/messages/{message_id}", response_model=EmailMessageResponse)
async def get_email_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific email message
    """
    message = db.query(EmailMessage).join(
        EmailConfig, EmailMessage.config_id == EmailConfig.id
    ).filter(
        EmailMessage.id == message_id,
        EmailConfig.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email message not found"
        )
    
    return message
