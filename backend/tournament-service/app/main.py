from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import atexit

from .api import router
from .database import create_tables
from .events import start_event_subscriber, stop_event_subscriber
from .models import Tournament

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Tournament Service", version="1.0.0")

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
    logger.info("Starting Tournament Service...")
    create_tables()
    logger.info("Database tables created/verified")
    
    # Create default tournament if it doesn't exist
    from .database import SessionLocal
    db = SessionLocal()
    try:
        default_tournament = db.query(Tournament).filter(Tournament.id == 1).first()
        if not default_tournament:
            default_tournament = Tournament(name="Default Tournament")
            db.add(default_tournament)
            db.commit()
            logger.info("Created default tournament")
    finally:
        db.close()
    
    # Start event subscriber
    start_event_subscriber()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Tournament Service...")
    stop_event_subscriber()

# Register cleanup on exit
atexit.register(stop_event_subscriber)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "tournament-service"}