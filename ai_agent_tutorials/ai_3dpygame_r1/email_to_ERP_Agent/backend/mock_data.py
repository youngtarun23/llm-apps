"""
Mock data initialization for development and testing.
"""
import json
import os
from datetime import datetime, timedelta

from models.sku import InventoryItem
from inventory_validator.validator import InventoryRepository
from erp_integration.erp_client import MockERPClient


def initialize_mock_data():
    """
    Initialize mock data for development and testing.
    """
    print("Initializing mock data...")
    
    # Create mock inventory data
    inventory_repository = InventoryRepository()
    
    # Sample inventory items
    inventory_items = [
        InventoryItem(
            sku_code="SKU001",
            name="Widget A",
            description="Standard widget with basic features",
            quantity=100,
            price=19.99,
            category="Widgets"
        ),
        InventoryItem(
            sku_code="SKU002",
            name="Widget B Pro",
            description="Professional grade widget with advanced features",
            quantity=50,
            price=49.99,
            category="Widgets"
        ),
        InventoryItem(
            sku_code="SKU003",
            name="Gadget X",
            description="Compact gadget for everyday use",
            quantity=75,
            price=29.99,
            category="Gadgets"
        ),
        InventoryItem(
            sku_code="SKU004",
            name="Gadget Y Plus",
            description="Enhanced gadget with extended battery life",
            quantity=30,
            price=59.99,
            category="Gadgets"
        ),
        InventoryItem(
            sku_code="SKU005",
            name="Tool Z",
            description="Multi-purpose tool for professionals",
            quantity=25,
            price=79.99,
            category="Tools"
        ),
        InventoryItem(
            sku_code="SKU006",
            name="Tool Z Mini",
            description="Compact version of the Tool Z",
            quantity=40,
            price=39.99,
            category="Tools"
        ),
        InventoryItem(
            sku_code="SKU007",
            name="Accessory Pack",
            description="Set of accessories compatible with all widgets",
            quantity=60,
            price=15.99,
            category="Accessories"
        ),
        InventoryItem(
            sku_code="SKU008",
            name="Premium Accessory Pack",
            description="Premium accessories for professional widgets",
            quantity=20,
            price=29.99,
            category="Accessories"
        ),
        InventoryItem(
            sku_code="SKU009",
            name="Connector Kit",
            description="Universal connectors for all gadgets",
            quantity=45,
            price=12.99,
            category="Accessories"
        ),
        InventoryItem(
            sku_code="SKU010",
            name="Power Adapter",
            description="High-capacity power adapter for all devices",
            quantity=35,
            price=24.99,
            category="Accessories"
        )
    ]
    
    # Add inventory items to repository
    inventory_repository.add_mock_data(inventory_items)
    print(f"Added {len(inventory_items)} inventory items to mock repository")
    
    # Create mock ERP client
    erp_client = MockERPClient()
    
    # Create directories for mock data
    os.makedirs("tokens", exist_ok=True)
    os.makedirs("credentials", exist_ok=True)
    
    # Create mock Gmail credentials
    gmail_credentials = {
        "installed": {
            "client_id": "mock-client-id.apps.googleusercontent.com",
            "project_id": "mock-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "mock-client-secret",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }
    
    with open("credentials/gmail_credentials.json", "w") as f:
        json.dump(gmail_credentials, f)
    
    print("Mock data initialization complete")
    
    return {
        "inventory_repository": inventory_repository,
        "erp_client": erp_client
    }


if __name__ == "__main__":
    initialize_mock_data()
