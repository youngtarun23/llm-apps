from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime

from database import Base

class EmailConfig(Base):
    """Email configuration model for storing email processing settings"""
    __tablename__ = "email_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    email_address = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    labels_to_monitor = Column(String)  # Comma-separated list of Gmail labels
    polling_interval = Column(Integer, default=300)  # Seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="email_configs")
    company = relationship("Company", back_populates="email_configs")
    messages = relationship("EmailMessage", back_populates="config")

class EmailMessage(Base):
    """Email message model for storing processed emails"""
    __tablename__ = "email_messages"

    id = Column(Integer, primary_key=True, index=True)
    config_id = Column(Integer, ForeignKey("email_configs.id"), index=True)
    message_id = Column(String, unique=True, index=True)  # Gmail message ID
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    body_text = Column(Text)
    body_html = Column(Text)
    received_at = Column(DateTime(timezone=True))
    processed_at = Column(DateTime(timezone=True))
    processing_status = Column(String)  # "pending", "processing", "success", "failed"
    extracted_data = Column(JSON)  # JSON data extracted from email
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    config = relationship("EmailConfig", back_populates="messages")
    processing_results = relationship("EmailProcessingResult", back_populates="message")

class EmailProcessingResult(Base):
    """Email processing result model for storing processing outcomes"""
    __tablename__ = "email_processing_results"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("email_messages.id"), index=True)
    erp_entry_id = Column(Integer, ForeignKey("erp_entries.id"), nullable=True)
    status = Column(String)  # "success", "failed", "partial"
    error_message = Column(Text, nullable=True)
    processing_details = Column(JSON)  # JSON data with processing details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    message = relationship("EmailMessage", back_populates="processing_results")
    erp_entry = relationship("ERPEntry", back_populates="email_result")

# Pydantic models for API
class EmailConfigCreate(BaseModel):
    email_address: EmailStr
    labels_to_monitor: str
    polling_interval: int = 300

class EmailConfigUpdate(BaseModel):
    labels_to_monitor: Optional[str] = None
    polling_interval: Optional[int] = None
    is_active: Optional[bool] = None

class EmailConfigResponse(BaseModel):
    id: int
    email_address: str
    labels_to_monitor: str
    polling_interval: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class EmailMessageResponse(BaseModel):
    id: int
    message_id: str
    sender: str
    recipient: str
    subject: str
    received_at: datetime
    processing_status: str
    processed_at: Optional[datetime] = None
    extracted_data: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class ExtractedSKUData(BaseModel):
    sku: str
    quantity: int
    description: Optional[str] = None
    unit_price: Optional[float] = None
    additional_details: Optional[Dict[str, Any]] = None
