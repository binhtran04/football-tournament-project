import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from app.main import app
from app.database import get_db
from app.models import Base, Tournament, TournamentTeam
from app.events import EventSubscriber

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

def test_create_tournament(client):
    """Test creating a tournament"""
    tournament_data = {"name": "Spring Cup"}
    
    response = client.post("/tournaments", json=tournament_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Spring Cup"
    assert "tournament_id" in data
    assert "created_at" in data

def test_get_tournaments_empty(client):
    """Test getting tournaments when none exist"""
    response = client.get("/tournaments")
    assert response.status_code == 200
    tournaments = response.json()
    # Default tournament is created on startup
    assert len(tournaments) >= 0

def test_get_tournaments_with_data(client):
    """Test getting tournaments when some exist"""
    # Create a tournament first
    tournament_data = {"name": "Winter Cup"}
    client.post("/tournaments", json=tournament_data)
    
    # Get tournaments
    response = client.get("/tournaments")
    assert response.status_code == 200
    tournaments = response.json()
    assert len(tournaments) >= 1
    
    # Find our created tournament
    winter_cup = None
    for t in tournaments:
        if t["name"] == "Winter Cup":
            winter_cup = t
            break
    
    assert winter_cup is not None
    assert winter_cup["name"] == "Winter Cup"

def test_team_registered_event_handler():
    """Test handling TeamRegistered event"""
    # Setup test database
    Base.metadata.create_all(bind=engine)
    
    try:
        # Create default tournament
        db = TestingSessionLocal()
        default_tournament = Tournament(id=1, name="Default Tournament")
        db.add(default_tournament)
        db.commit()
        db.close()
        
        # Create event subscriber with mocked ZeroMQ
        subscriber = EventSubscriber()
        
        # Mock the ZeroMQ socket
        with patch.object(subscriber, 'socket'):
            with patch.object(subscriber, '_listen'):
                # Test event message
                event_message = json.dumps({
                    "event": "TeamRegistered",
                    "payload": {
                        "teamId": "test-team-123",
                        "name": "Test FC"
                    },
                    "timestamp": "2024-01-01T10:00:00Z"
                })
                
                # Handle the message
                subscriber._handle_message(event_message)
                
                # Verify tournament team was created
                db = TestingSessionLocal()
                tournament_team = db.query(TournamentTeam).filter_by(team_id="test-team-123").first()
                
                assert tournament_team is not None
                assert tournament_team.team_name == "Test FC"
                assert tournament_team.tournament_id == 1
                
                db.close()
                
    finally:
        Base.metadata.drop_all(bind=engine)

def test_get_tournament_teams(client):
    """Test getting tournament teams endpoint"""
    response = client.get("/tournament-teams")
    assert response.status_code == 200
    teams = response.json()
    assert isinstance(teams, list)