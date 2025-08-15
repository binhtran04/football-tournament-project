from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TournamentCreate(BaseModel):
    name: str

class TournamentTeamResponse(BaseModel):
    id: int
    team_id: str
    team_name: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TournamentResponse(BaseModel):
    id: int
    tournament_id: str
    name: str
    created_at: Optional[datetime] = None
    teams: List[TournamentTeamResponse] = []
    
    class Config:
        from_attributes = True