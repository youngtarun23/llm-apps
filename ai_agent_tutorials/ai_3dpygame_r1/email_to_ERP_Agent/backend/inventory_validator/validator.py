"""
Inventory validator module for validating SKUs against inventory.
"""
from typing import Dict, List, Optional, Tuple

from ..models.sku import SKUInfo, InventoryItem


class InventoryValidator:
    """
    Validator for SKUs against inventory.
    """
    def __init__(self, inventory_repository):
        """
        Initialize the inventory validator.
        
        Args:
            inventory_repository: Repository for accessing inventory data
        """
        self.inventory_repository = inventory_repository
    
    def validate_skus(self, skus: List[SKUInfo]) -> Tuple[List[SKUInfo], List[SKUInfo]]:
        """
        Validate SKUs against inventory.
        
        Args:
            skus: List of SKUInfo objects to validate
            
        Returns:
            Tuple of valid and invalid SKUs
        """
        valid_skus = []
        invalid_skus = []
        
        for sku in skus:
            # Check if SKU exists in inventory
            inventory_item = self.inventory_repository.get_by_sku(sku.sku_code)
            
            if inventory_item:
                # Check if quantity is available
                if inventory_item.quantity >= sku.quantity:
                    sku.validated = True
                    valid_skus.append(sku)
                else:
                    invalid_skus.append(sku)
            else:
                invalid_skus.append(sku)
        
        return valid_skus, invalid_skus
    
    def get_inventory_items(self, skus: List[SKUInfo]) -> Dict[str, InventoryItem]:
        """
        Get inventory items for SKUs.
        
        Args:
            skus: List of SKUInfo objects
            
        Returns:
            Dictionary mapping SKU codes to InventoryItem objects
        """
        inventory_items = {}
        
        for sku in skus:
            inventory_item = self.inventory_repository.get_by_sku(sku.sku_code)
            if inventory_item:
                inventory_items[sku.sku_code] = inventory_item
        
        return inventory_items


class InventoryRepository:
    """
    Repository for accessing inventory data.
    """
    def __init__(self, db_session=None):
        """
        Initialize the inventory repository.
        
        Args:
            db_session: Database session
        """
        self.db_session = db_session
        self._mock_inventory = {}  # For mock implementation
    
    def get_by_sku(self, sku_code: str) -> Optional[InventoryItem]:
        """
        Get inventory item by SKU code.
        
        Args:
            sku_code: SKU code
            
        Returns:
            InventoryItem if found, None otherwise
        """
        if self.db_session:
            # Implement database query
            pass
        else:
            # Return mock data
            return self._mock_inventory.get(sku_code)
    
    def get_all(self) -> List[InventoryItem]:
        """
        Get all inventory items.
        
        Returns:
            List of InventoryItem objects
        """
        if self.db_session:
            # Implement database query
            pass
        else:
            # Return mock data
            return list(self._mock_inventory.values())
    
    def update_quantity(self, sku_code: str, quantity: int) -> bool:
        """
        Update inventory item quantity.
        
        Args:
            sku_code: SKU code
            quantity: New quantity
            
        Returns:
            True if successful, False otherwise
        """
        if self.db_session:
            # Implement database update
            pass
        else:
            # Update mock data
            if sku_code in self._mock_inventory:
                self._mock_inventory[sku_code].quantity = quantity
                return True
            return False
    
    def add_mock_data(self, inventory_items: List[InventoryItem]):
        """
        Add mock inventory data.
        
        Args:
            inventory_items: List of InventoryItem objects
        """
        for item in inventory_items:
            self._mock_inventory[item.sku_code] = item
