"""
SKU models for the application.
"""
from typing import Optional

from pydantic import BaseModel


class SKUInfo:
    """
    SKU information model.
    """
    sku_code: str
    quantity: int
    source_email_id: Optional[str]
    validated: bool
    erp_entry_id: Optional[str]
    
    def __init__(
        self,
        sku_code: str,
        quantity: int,
        source_email_id: Optional[str] = None,
        validated: bool = False,
        erp_entry_id: Optional[str] = None
    ):
        self.sku_code = sku_code
        self.quantity = quantity
        self.source_email_id = source_email_id
        self.validated = validated
        self.erp_entry_id = erp_entry_id
    
    def to_dict(self):
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation of the SKU information
        """
        return {
            "sku_code": self.sku_code,
            "quantity": self.quantity,
            "source_email_id": self.source_email_id,
            "validated": self.validated,
            "erp_entry_id": self.erp_entry_id
        }


class InventoryItem:
    """
    Inventory item model.
    """
    sku_code: str
    name: str
    description: str
    quantity: int
    price: float
    category: str
    
    def __init__(
        self,
        sku_code: str,
        name: str,
        description: str,
        quantity: int,
        price: float,
        category: str
    ):
        self.sku_code = sku_code
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.category = category
    
    def to_dict(self):
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation of the inventory item
        """
        return {
            "sku_code": self.sku_code,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "price": self.price,
            "category": self.category
        }


class SKUResponse(BaseModel):
    """
    SKU response model for API.
    """
    sku_code: str
    quantity: int
    source_email_id: Optional[str]
    validated: bool
    erp_entry_id: Optional[str]


class InventoryItemResponse(BaseModel):
    """
    Inventory item response model for API.
    """
    sku_code: str
    name: str
    description: str
    quantity: int
    price: float
    category: str
