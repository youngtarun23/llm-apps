"""
API routes for ERP integration.
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, List, Any

from ..auth.oauth import get_current_user
from ..erp_integration.erp_client import SAPClient, NetSuiteClient, CustomERPClient, MockERPClient
from ..models.sku import SKUInfo, SKUResponse

router = APIRouter(
    prefix="/api/erp",
    tags=["erp"]
)


@router.post("/submit", response_model=SKUResponse)
async def submit_to_erp(
    sku_data: Dict[str, Any] = Body(...),
    current_user = Depends(get_current_user)
):
    """
    Submit SKU to ERP system.
    """
    try:
        # Create SKU info
        sku = SKUInfo(
            sku_code=sku_data["sku_code"],
            quantity=sku_data["quantity"],
            source_email_id=sku_data.get("source_email_id"),
            validated=sku_data.get("validated", False),
            erp_entry_id=None
        )
        
        # Get ERP client based on user settings
        # In a real implementation, we would get these from user settings
        erp_type = sku_data.get("erp_type", "mock")
        api_url = sku_data.get("api_url", "https://erp-api.example.com/v1")
        api_key = sku_data.get("api_key", "mock-api-key")
        
        if erp_type == "sap":
            erp_client = SAPClient(api_url, api_key)
        elif erp_type == "netsuite":
            erp_client = NetSuiteClient(api_url, api_key)
        elif erp_type == "custom":
            erp_client = CustomERPClient(api_url, api_key)
        else:
            erp_client = MockERPClient()
        
        # Submit SKU to ERP
        erp_entry_id = erp_client.submit_sku(sku)
        
        if not erp_entry_id:
            raise HTTPException(status_code=500, detail="Failed to submit SKU to ERP")
        
        # Update SKU with ERP entry ID
        sku.erp_entry_id = erp_entry_id
        
        # Convert to response model
        sku_response = SKUResponse(
            sku_code=sku.sku_code,
            quantity=sku.quantity,
            source_email_id=sku.source_email_id,
            validated=sku.validated,
            erp_entry_id=sku.erp_entry_id
        )
        
        return sku_response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{erp_entry_id}", response_model=Dict[str, Any])
async def get_erp_status(
    erp_entry_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get ERP status for entry.
    """
    try:
        # Get ERP client based on user settings
        # In a real implementation, we would get these from user settings
        erp_type = "mock"  # This would come from user settings
        api_url = "https://erp-api.example.com/v1"
        api_key = "mock-api-key"
        
        if erp_type == "sap":
            erp_client = SAPClient(api_url, api_key)
        elif erp_type == "netsuite":
            erp_client = NetSuiteClient(api_url, api_key)
        elif erp_type == "custom":
            erp_client = CustomERPClient(api_url, api_key)
        else:
            erp_client = MockERPClient()
        
        # Get status from ERP
        status = erp_client.get_sku_status(erp_entry_id)
        
        return status
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=List[SKUResponse])
async def batch_submit_to_erp(
    skus_data: List[Dict[str, Any]] = Body(...),
    current_user = Depends(get_current_user)
):
    """
    Submit multiple SKUs to ERP system.
    """
    try:
        # Get ERP client based on user settings
        # In a real implementation, we would get these from user settings
        erp_type = "mock"  # This would come from user settings
        api_url = "https://erp-api.example.com/v1"
        api_key = "mock-api-key"
        
        if erp_type == "sap":
            erp_client = SAPClient(api_url, api_key)
        elif erp_type == "netsuite":
            erp_client = NetSuiteClient(api_url, api_key)
        elif erp_type == "custom":
            erp_client = CustomERPClient(api_url, api_key)
        else:
            erp_client = MockERPClient()
        
        # Process each SKU
        sku_responses = []
        for sku_data in skus_data:
            # Create SKU info
            sku = SKUInfo(
                sku_code=sku_data["sku_code"],
                quantity=sku_data["quantity"],
                source_email_id=sku_data.get("source_email_id"),
                validated=sku_data.get("validated", False),
                erp_entry_id=None
            )
            
            # Submit SKU to ERP
            erp_entry_id = erp_client.submit_sku(sku)
            
            if erp_entry_id:
                # Update SKU with ERP entry ID
                sku.erp_entry_id = erp_entry_id
            
            # Convert to response model
            sku_response = SKUResponse(
                sku_code=sku.sku_code,
                quantity=sku.quantity,
                source_email_id=sku.source_email_id,
                validated=sku.validated,
                erp_entry_id=sku.erp_entry_id
            )
            
            sku_responses.append(sku_response)
        
        return sku_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
