// Mock data for the Email to ERP Agent application

export interface EmailMessage {
  id: number;
  message_id: string;
  sender: string;
  recipient: string;
  subject: string;
  received_at: string;
  processing_status: 'pending' | 'processing' | 'success' | 'failed';
  processed_at?: string;
  extracted_data?: ExtractedSKUData[];
}

export interface ExtractedSKUData {
  sku: string;
  quantity: number;
  description?: string;
  unit_price?: number;
  additional_details?: Record<string, any>;
}

export interface InventoryItem {
  id: number;
  sku: string;
  name: string;
  description: string;
  quantity: number;
  unit_price: number;
  category: string;
  last_updated: string;
}

export interface ERPEntry {
  id: number;
  email_id: number;
  status: 'pending' | 'processed' | 'failed';
  created_at: string;
  updated_at: string;
  items: ExtractedSKUData[];
}

// Mock emails
export const mockEmails: EmailMessage[] = [
  {
    id: 1,
    message_id: 'msg_001',
    sender: 'supplier@example.com',
    recipient: 'orders@yourcompany.com',
    subject: 'New Order: SKUs 12345, 67890',
    received_at: '2025-02-25T10:30:00Z',
    processing_status: 'success',
    processed_at: '2025-02-25T10:32:00Z',
    extracted_data: [
      {
        sku: 'SKU12345',
        quantity: 10,
        description: 'Premium Widgets',
        unit_price: 29.99
      },
      {
        sku: 'SKU67890',
        quantity: 5,
        description: 'Deluxe Gadgets',
        unit_price: 49.99
      }
    ]
  },
  {
    id: 2,
    message_id: 'msg_002',
    sender: 'vendor@example.org',
    recipient: 'orders@yourcompany.com',
    subject: 'Order Confirmation #54321',
    received_at: '2025-02-25T14:15:00Z',
    processing_status: 'success',
    processed_at: '2025-02-25T14:17:00Z',
    extracted_data: [
      {
        sku: 'SKU54321',
        quantity: 20,
        description: 'Standard Components',
        unit_price: 12.50
      }
    ]
  },
  {
    id: 3,
    message_id: 'msg_003',
    sender: 'sales@competitor.com',
    recipient: 'info@yourcompany.com',
    subject: 'Partnership Opportunity',
    received_at: '2025-02-26T09:00:00Z',
    processing_status: 'failed',
    processed_at: '2025-02-26T09:01:00Z'
  },
  {
    id: 4,
    message_id: 'msg_004',
    sender: 'distributor@example.net',
    recipient: 'orders@yourcompany.com',
    subject: 'Urgent Order: SKU98765',
    received_at: '2025-02-26T11:45:00Z',
    processing_status: 'pending'
  },
  {
    id: 5,
    message_id: 'msg_005',
    sender: 'warehouse@example.com',
    recipient: 'orders@yourcompany.com',
    subject: 'Inventory Update: Multiple SKUs',
    received_at: '2025-02-26T13:20:00Z',
    processing_status: 'processing'
  }
];

// Mock inventory items
export const mockInventory: InventoryItem[] = [
  {
    id: 1,
    sku: 'SKU12345',
    name: 'Premium Widgets',
    description: 'High-quality widgets for professional use',
    quantity: 250,
    unit_price: 29.99,
    category: 'Widgets',
    last_updated: '2025-02-24T16:00:00Z'
  },
  {
    id: 2,
    sku: 'SKU67890',
    name: 'Deluxe Gadgets',
    description: 'Advanced gadgets with premium features',
    quantity: 120,
    unit_price: 49.99,
    category: 'Gadgets',
    last_updated: '2025-02-25T09:30:00Z'
  },
  {
    id: 3,
    sku: 'SKU54321',
    name: 'Standard Components',
    description: 'Basic components for everyday use',
    quantity: 500,
    unit_price: 12.50,
    category: 'Components',
    last_updated: '2025-02-25T14:45:00Z'
  },
  {
    id: 4,
    sku: 'SKU98765',
    name: 'Economy Parts',
    description: 'Affordable parts for budget-conscious customers',
    quantity: 0,
    unit_price: 8.99,
    category: 'Parts',
    last_updated: '2025-02-26T10:15:00Z'
  },
  {
    id: 5,
    sku: 'SKU24680',
    name: 'Luxury Accessories',
    description: 'High-end accessories for discerning customers',
    quantity: 75,
    unit_price: 89.99,
    category: 'Accessories',
    last_updated: '2025-02-26T11:00:00Z'
  }
];

// Mock ERP entries
export const mockERPEntries: ERPEntry[] = [
  {
    id: 1,
    email_id: 1,
    status: 'processed',
    created_at: '2025-02-25T10:32:00Z',
    updated_at: '2025-02-25T10:35:00Z',
    items: [
      {
        sku: 'SKU12345',
        quantity: 10,
        description: 'Premium Widgets',
        unit_price: 29.99
      },
      {
        sku: 'SKU67890',
        quantity: 5,
        description: 'Deluxe Gadgets',
        unit_price: 49.99
      }
    ]
  },
  {
    id: 2,
    email_id: 2,
    status: 'processed',
    created_at: '2025-02-25T14:17:00Z',
    updated_at: '2025-02-25T14:20:00Z',
    items: [
      {
        sku: 'SKU54321',
        quantity: 20,
        description: 'Standard Components',
        unit_price: 12.50
      }
    ]
  },
  {
    id: 3,
    email_id: 4,
    status: 'pending',
    created_at: '2025-02-26T11:46:00Z',
    updated_at: '2025-02-26T11:46:00Z',
    items: [
      {
        sku: 'SKU98765',
        quantity: 15,
        description: 'Economy Parts',
        unit_price: 8.99
      }
    ]
  }
];

// Mock statistics for dashboard
export const mockStats = {
  totalEmails: 5,
  processedEmails: 2,
  pendingEmails: 1,
  failedEmails: 1,
  processingEmails: 1,
  inventoryAlerts: 1,
  successRate: 66.7
};
