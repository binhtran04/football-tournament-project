import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'team_user')}:{os.getenv('DB_PASSWORD', 'team_password')}@{os.getenv('TEAM_DB_HOST', 'team-db')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'team_db')}"

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