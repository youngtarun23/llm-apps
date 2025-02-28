from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging
import os
from dotenv import load_dotenv

# Import modules from our application
from database import get_db, init_db
from auth.oauth import get_current_user, User
from mock_data import initialize_mock_data
from routers.emails import router as email_router
from routers.erp import router as erp_router
from routers.inventory import router as inventory_router
from routers.auth import router as auth_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Email to ERP Agent API",
    description="API for Email to ERP Agent system",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for mock data
mock_data = {}

# Include routers
app.include_router(email_router)
app.include_router(erp_router)
app.include_router(inventory_router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and other startup tasks"""
    logger.info("Starting up Email to ERP Agent API")
    
    # Initialize mock data for development
    global mock_data
    mock_data = initialize_mock_data()
    
    # Initialize database
    try:
        init_db()
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}. Using mock data only.")

@app.on_event("shutdown")
async def shutdown_event():
    """Perform cleanup on shutdown"""
    logger.info("Shutting down Email to ERP Agent API")

@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {"status": "online", "message": "Email to ERP Agent API is running"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
