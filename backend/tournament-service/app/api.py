from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from .database import get_db
from .models import Tournament, TournamentTeam
from .schemas import TournamentCreate, TournamentResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/tournaments", response_model=TournamentResponse)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    try:
        # Create new tournament
        db_tournament = Tournament(name=tournament.name)
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
        
        logger.info(f"Created tournament: {db_tournament.name} with ID: {db_tournament.tournament_id}")
        
        return db_tournament
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create tournament: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create tournament")

@router.get("/tournaments", response_model=List[TournamentResponse])
def get_tournaments(db: Session = Depends(get_db)):
    try:
        tournaments = db.query(Tournament).all()
        logger.info(f"Retrieved {len(tournaments)} tournaments")
        return tournaments
    except Exception as e:
        logger.error(f"Failed to retrieve tournaments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tournaments")

@router.get("/tournament-teams")
def get_tournament_teams(db: Session = Depends(get_db)):
    """Get all tournament team registrations (for debugging/testing)"""
    try:
        teams = db.query(TournamentTeam).all()
        logger.info(f"Retrieved {len(teams)} tournament team entries")
        return [team.to_dict() for team in teams]
    except Exception as e:
        logger.error(f"Failed to retrieve tournament teams: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tournament teams")