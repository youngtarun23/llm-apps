"""
API routes for inventory management.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from ..auth.oauth import get_current_user
from ..inventory_validator.validator import InventoryRepository
from ..models.sku import InventoryItemResponse

router = APIRouter(
    prefix="/api/inventory",
    tags=["inventory"]
)


@router.get("/", response_model=List[InventoryItemResponse])
async def get_inventory_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    current_user = Depends(get_current_user)
):
    """
    Get inventory items.
    """
    try:
        # Create inventory repository
        inventory_repository = InventoryRepository()
        
        # Get all inventory items
        inventory_items = inventory_repository.get_all()
        
        # Filter by category if specified
        if category:
            inventory_items = [item for item in inventory_items if item.category == category]
        
        # Convert to response model
        inventory_responses = [
            InventoryItemResponse(
                sku_code=item.sku_code,
                name=item.name,
                description=item.description,
                quantity=item.quantity,
                price=item.price,
                category=item.category
            ) for item in inventory_items
        ]
        
        return inventory_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{sku_code}", response_model=InventoryItemResponse)
async def get_inventory_item(
    sku_code: str,
    current_user = Depends(get_current_user)
):
    """
    Get inventory item by SKU code.
    """
    try:
        # Create inventory repository
        inventory_repository = InventoryRepository()
        
        # Get inventory item
        inventory_item = inventory_repository.get_by_sku(sku_code)
        
        if not inventory_item:
            raise HTTPException(status_code=404, detail=f"Inventory item with SKU {sku_code} not found")
        
        # Convert to response model
        inventory_response = InventoryItemResponse(
            sku_code=inventory_item.sku_code,
            name=inventory_item.name,
            description=inventory_item.description,
            quantity=inventory_item.quantity,
            price=inventory_item.price,
            category=inventory_item.category
        )
        
        return inventory_response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{sku_code}/quantity", response_model=InventoryItemResponse)
async def update_inventory_quantity(
    sku_code: str,
    quantity: int,
    current_user = Depends(get_current_user)
):
    """
    Update inventory item quantity.
    """
    try:
        # Create inventory repository
        inventory_repository = InventoryRepository()
        
        # Get inventory item
        inventory_item = inventory_repository.get_by_sku(sku_code)
        
        if not inventory_item:
            raise HTTPException(status_code=404, detail=f"Inventory item with SKU {sku_code} not found")
        
        # Update quantity
        success = inventory_repository.update_quantity(sku_code, quantity)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to update quantity for SKU {sku_code}")
        
        # Get updated inventory item
        updated_item = inventory_repository.get_by_sku(sku_code)
        
        # Convert to response model
        inventory_response = InventoryItemResponse(
            sku_code=updated_item.sku_code,
            name=updated_item.name,
            description=updated_item.description,
            quantity=updated_item.quantity,
            price=updated_item.price,
            category=updated_item.category
        )
        
        return inventory_response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
