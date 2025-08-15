from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional
import uuid

Base = declarative_base()

class Tournament(Base):
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to tournament teams
    teams = relationship("TournamentTeam", back_populates="tournament")
    
    def to_dict(self):
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class TournamentTeam(Base):
    __tablename__ = "tournament_teams"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    team_id = Column(String, nullable=False)  # External team ID from team-service
    team_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to tournament
    tournament = relationship("Tournament", back_populates="teams")
    
    def to_dict(self):
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "team_id": self.team_id,
            "team_name": self.team_name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }