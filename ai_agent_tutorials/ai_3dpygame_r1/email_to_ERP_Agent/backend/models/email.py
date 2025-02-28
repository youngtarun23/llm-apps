"""
Email models for the application.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Attachment:
    """
    Email attachment model.
    """
    id: str
    filename: str
    mime_type: str
    size: int
    content: Optional[bytes] = None
    
    def __init__(
        self, 
        id: str, 
        filename: str, 
        mime_type: str, 
        size: int, 
        content: Optional[bytes] = None
    ):
        self.id = id
        self.filename = filename
        self.mime_type = mime_type
        self.size = size
        self.content = content


class EmailMessage:
    """
    Email message model.
    """
    id: str
    thread_id: str
    subject: str
    from_email: str
    date: datetime
    body: str
    attachments: List[Attachment]
    labels: List[str]
    processed: bool
    
    def __init__(
        self,
        id: str,
        thread_id: str,
        subject: str,
        from_email: str,
        date: datetime,
        body: str,
        attachments: List[Attachment],
        labels: List[str],
        processed: bool = False
    ):
        self.id = id
        self.thread_id = thread_id
        self.subject = subject
        self.from_email = from_email
        self.date = date
        self.body = body
        self.attachments = attachments
        self.labels = labels
        self.processed = processed
    
    def to_dict(self):
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation of the email message
        """
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "subject": self.subject,
            "from_email": self.from_email,
            "date": self.date.isoformat(),
            "body": self.body[:500] + "..." if len(self.body) > 500 else self.body,  # Truncate long bodies
            "attachments": [
                {
                    "id": attachment.id,
                    "filename": attachment.filename,
                    "mime_type": attachment.mime_type,
                    "size": attachment.size
                } for attachment in self.attachments
            ],
            "labels": self.labels,
            "processed": self.processed
        }


class EmailResponse(BaseModel):
    """
    Email response model for API.
    """
    id: str
    thread_id: str
    subject: str
    from_email: str
    date: str
    body_preview: str
    attachment_count: int
    labels: List[str]
    processed: bool
