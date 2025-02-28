"""
User models for the application.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User:
    """
    User model.
    """
    id: str
    email: str
    first_name: str
    last_name: str
    company: str
    created_at: datetime
    updated_at: datetime
    
    def __init__(
        self,
        id: str,
        email: str,
        first_name: str,
        last_name: str,
        company: str,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation of the user
        """
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class UserCreate(BaseModel):
    """
    User creation model.
    """
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company: str


class UserResponse(BaseModel):
    """
    User response model.
    """
    id: str
    email: str
    first_name: str
    last_name: str
    company: str
    created_at: str
    updated_at: str


class TokenResponse(BaseModel):
    """
    Token response model.
    """
    access_token: str
    token_type: str
