"""
ERP client module for integrating with ERP systems.
"""
import json
import logging
import requests
from typing import Dict, List, Optional, Any

from ..models.sku import SKUInfo


class ERPClient:
    """
    Base class for ERP clients.
    """
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize the ERP client.
        
        Args:
            api_url: ERP API URL
            api_key: ERP API key
        """
        self.api_url = api_url
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def submit_sku(self, sku: SKUInfo) -> Optional[str]:
        """
        Submit SKU to ERP system.
        
        Args:
            sku: SKUInfo object
            
        Returns:
            ERP entry ID if successful, None otherwise
        """
        raise NotImplementedError("Subclasses must implement submit_sku")
    
    def get_sku_status(self, erp_entry_id: str) -> Dict[str, Any]:
        """
        Get SKU status from ERP system.
        
        Args:
            erp_entry_id: ERP entry ID
            
        Returns:
            Dictionary with status information
        """
        raise NotImplementedError("Subclasses must implement get_sku_status")


class SAPClient(ERPClient):
    """
    Client for SAP ERP system.
    """
    def submit_sku(self, sku: SKUInfo) -> Optional[str]:
        """
        Submit SKU to SAP ERP system.
        
        Args:
            sku: SKUInfo object
            
        Returns:
            ERP entry ID if successful, None otherwise
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "sku_code": sku.sku_code,
                "quantity": sku.quantity,
                "source_email_id": sku.source_email_id
            }
            
            response = requests.post(
                f"{self.api_url}/items",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                return result.get("entry_id")
            else:
                self.logger.error(f"Failed to submit SKU to SAP: {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error submitting SKU to SAP: {str(e)}")
            return None
    
    def get_sku_status(self, erp_entry_id: str) -> Dict[str, Any]:
        """
        Get SKU status from SAP ERP system.
        
        Args:
            erp_entry_id: ERP entry ID
            
        Returns:
            Dictionary with status information
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(
                f"{self.api_url}/items/{erp_entry_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get SKU status from SAP: {response.text}")
                return {"status": "error", "message": response.text}
        
        except Exception as e:
            self.logger.error(f"Error getting SKU status from SAP: {str(e)}")
            return {"status": "error", "message": str(e)}


class NetSuiteClient(ERPClient):
    """
    Client for NetSuite ERP system.
    """
    def submit_sku(self, sku: SKUInfo) -> Optional[str]:
        """
        Submit SKU to NetSuite ERP system.
        
        Args:
            sku: SKUInfo object
            
        Returns:
            ERP entry ID if successful, None otherwise
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"NLAuth nlauth_account=YOUR_ACCOUNT,nlauth_email=YOUR_EMAIL,nlauth_signature={self.api_key}"
            }
            
            data = {
                "item": {
                    "sku": sku.sku_code,
                    "quantity": sku.quantity,
                    "email_reference": sku.source_email_id
                }
            }
            
            response = requests.post(
                f"{self.api_url}/record/v1/salesorder",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                return result.get("id")
            else:
                self.logger.error(f"Failed to submit SKU to NetSuite: {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error submitting SKU to NetSuite: {str(e)}")
            return None
    
    def get_sku_status(self, erp_entry_id: str) -> Dict[str, Any]:
        """
        Get SKU status from NetSuite ERP system.
        
        Args:
            erp_entry_id: ERP entry ID
            
        Returns:
            Dictionary with status information
        """
        try:
            headers = {
                "Authorization": f"NLAuth nlauth_account=YOUR_ACCOUNT,nlauth_email=YOUR_EMAIL,nlauth_signature={self.api_key}"
            }
            
            response = requests.get(
                f"{self.api_url}/record/v1/salesorder/{erp_entry_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get SKU status from NetSuite: {response.text}")
                return {"status": "error", "message": response.text}
        
        except Exception as e:
            self.logger.error(f"Error getting SKU status from NetSuite: {str(e)}")
            return {"status": "error", "message": str(e)}


class CustomERPClient(ERPClient):
    """
    Client for custom ERP system.
    """
    def submit_sku(self, sku: SKUInfo) -> Optional[str]:
        """
        Submit SKU to custom ERP system.
        
        Args:
            sku: SKUInfo object
            
        Returns:
            ERP entry ID if successful, None otherwise
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key
            }
            
            data = {
                "sku_code": sku.sku_code,
                "quantity": sku.quantity,
                "source": "email",
                "source_id": sku.source_email_id
            }
            
            response = requests.post(
                f"{self.api_url}/orders",
                headers=headers,
                json=data
            )
            
            if response.status_code in (200, 201):
                result = response.json()
                return result.get("order_id")
            else:
                self.logger.error(f"Failed to submit SKU to custom ERP: {response.text}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error submitting SKU to custom ERP: {str(e)}")
            return None
    
    def get_sku_status(self, erp_entry_id: str) -> Dict[str, Any]:
        """
        Get SKU status from custom ERP system.
        
        Args:
            erp_entry_id: ERP entry ID
            
        Returns:
            Dictionary with status information
        """
        try:
            headers = {
                "X-API-Key": self.api_key
            }
            
            response = requests.get(
                f"{self.api_url}/orders/{erp_entry_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get SKU status from custom ERP: {response.text}")
                return {"status": "error", "message": response.text}
        
        except Exception as e:
            self.logger.error(f"Error getting SKU status from custom ERP: {str(e)}")
            return {"status": "error", "message": str(e)}


class MockERPClient(ERPClient):
    """
    Mock ERP client for testing.
    """
    def __init__(self):
        """
        Initialize the mock ERP client.
        """
        super().__init__("mock://erp-api", "mock-api-key")
        self.entries = {}
    
    def submit_sku(self, sku: SKUInfo) -> Optional[str]:
        """
        Submit SKU to mock ERP system.
        
        Args:
            sku: SKUInfo object
            
        Returns:
            ERP entry ID if successful, None otherwise
        """
        import uuid
        
        entry_id = str(uuid.uuid4())
        
        self.entries[entry_id] = {
            "id": entry_id,
            "sku_code": sku.sku_code,
            "quantity": sku.quantity,
            "source_email_id": sku.source_email_id,
            "status": "pending",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
        
        return entry_id
    
    def get_sku_status(self, erp_entry_id: str) -> Dict[str, Any]:
        """
        Get SKU status from mock ERP system.
        
        Args:
            erp_entry_id: ERP entry ID
            
        Returns:
            Dictionary with status information
        """
        if erp_entry_id in self.entries:
            return self.entries[erp_entry_id]
        else:
            return {"status": "error", "message": "Entry not found"}
