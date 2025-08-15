from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from .api import router
from .database import create_tables
from .events import get_publisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Team Service", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be more specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Team Service...")
    create_tables()
    logger.info("Database tables created/verified")
    
    # Initialize ZeroMQ publisher at startup
    try:
        publisher = get_publisher()
        logger.info("ZeroMQ publisher initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ZeroMQ publisher: {e}")
        raise

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "team-service"}