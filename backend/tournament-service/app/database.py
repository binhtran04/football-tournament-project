import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'tournament_user')}:{os.getenv('DB_PASSWORD', 'tournament_password')}@{os.getenv('TOURNAMENT_DB_HOST', 'tournament-db')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'tournament_db')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)