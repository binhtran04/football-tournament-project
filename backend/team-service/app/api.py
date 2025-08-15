from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from .database import get_db
from .models import Team
from .schemas import TeamCreate, TeamResponse
from .events import publish_team_registered

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/teams", response_model=TeamResponse)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    try:
        # Create new team
        db_team = Team(name=team.name)
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        
        logger.info(f"Created team: {db_team.name} with ID: {db_team.team_id}")
        
        # Publish TeamRegistered event
        team_data = db_team.to_dict()
        publish_team_registered(team_data)
        
        return db_team
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create team: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create team")

@router.get("/teams", response_model=List[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    try:
        teams = db.query(Team).all()
        logger.info(f"Retrieved {len(teams)} teams")
        return teams
    except Exception as e:
        logger.error(f"Failed to retrieve teams: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve teams")