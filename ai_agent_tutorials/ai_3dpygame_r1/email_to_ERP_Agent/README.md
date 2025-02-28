# Email to ERP Agent

An intelligent agent system that scans emails, extracts SKU details, and enters them into ERP systems via API. The system validates inventory and SKU codes, sending follow-up emails when necessary.

## Features

- **Email Scanning**: Automatically scan emails for order details and SKU information
- **ERP Integration**: Seamlessly enter extracted data into ERP systems via API
- **Inventory Validation**: Verify SKUs against inventory and cross-verify codes
- **Automated Follow-ups**: Send follow-up emails for missing or invalid SKUs
- **Multi-company Support**: Modular architecture that scales across multiple companies
- **Gmail Integration**: Easy setup via Gmail sign-up with appropriate permissions

## Project Structure

```
email_to_ERP_Agent/
├── backend/
│   ├── email_processor/      # Email scanning and data extraction
│   ├── erp_integration/      # ERP API integration
│   ├── inventory_validator/  # SKU and inventory validation
│   ├── email_sender/         # Follow-up email generation and sending
│   └── api/                  # Backend API endpoints
├── frontend/
│   ├── app/                  # Next.js app directory
│   ├── components/           # Reusable UI components with shadcn/ui
│   └── public/               # Static assets
└── docs/                     # Documentation
```

## Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: Next.js, TypeScript, shadcn/ui
- **Email Integration**: Gmail API
- **Authentication**: OAuth 2.0
- **Database**: PostgreSQL
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL
- Docker (optional)

### Installation

1. Clone the repository
2. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

### Configuration

1. Create a `.env` file in the backend directory with your configuration
2. Set up OAuth credentials for Gmail API

### Running the Application

#### Using the Run Scripts

We've provided convenient scripts to run both the backend and frontend:

1. Start the backend with mock data:
   ```
   python run_backend.py
   ```

2. Start the frontend:
   ```
   python run_frontend.py
   ```

#### Manual Start

Alternatively, you can start the services manually:

1. Start the backend:
   ```
   cd backend
   uvicorn main:app --reload
   ```
2. Start the frontend:
   ```
   cd frontend
   npm run dev
   ```

## Development Mode

The application currently uses mock data for development purposes. This allows you to test the functionality without setting up actual database connections or API integrations.

When running in development mode:
- A mock inventory with sample SKUs is automatically created
- Mock ERP clients are available for testing
- Gmail credentials are simulated
- No actual emails are sent or received
- No actual database connections are required

To switch to production mode, you'll need to:
1. Configure the database connection in `.env`
2. Set up real Gmail API credentials
3. Configure the actual ERP system API endpoints
4. Update the environment variables accordingly

## License

MIT
