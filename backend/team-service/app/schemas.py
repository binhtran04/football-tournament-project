from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TeamCreate(BaseModel):
    name: str

class TeamResponse(BaseModel):
    id: int
    team_id: str
    name: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True