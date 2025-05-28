"""
TicketConnect Backend - Main FastAPI Application
"""

import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="TicketConnect API",
    description="Peer-to-peer ticket reselling platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running
    """
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "message": "TicketConnect API is running",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to TicketConnect API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    logger.info("Starting TicketConnect API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 