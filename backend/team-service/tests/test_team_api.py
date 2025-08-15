import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from app.main import app
from app.database import get_db
from app.models import Base, Team

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

@patch('app.events.publish_team_registered')
def test_create_team(mock_publish, client):
    """Test creating a team"""
    team_data = {"name": "Helsinki FC"}
    
    response = client.post("/teams", json=team_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Helsinki FC"
    assert "team_id" in data
    assert "created_at" in data
    
    # Verify event publishing was called
    mock_publish.assert_called_once()
    call_args = mock_publish.call_args[0][0]
    assert call_args["name"] == "Helsinki FC"

def test_get_teams_empty(client):
    """Test getting teams when none exist"""
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []

@patch('app.events.publish_team_registered')
def test_get_teams_with_data(mock_publish, client):
    """Test getting teams when some exist"""
    # Create a team first
    team_data = {"name": "Oulu FC"}
    client.post("/teams", json=team_data)
    
    # Get teams
    response = client.get("/teams")
    assert response.status_code == 200
    teams = response.json()
    assert len(teams) == 1
    assert teams[0]["name"] == "Oulu FC"

@patch('app.events.publish_team_registered')
def test_create_multiple_teams(mock_publish, client):
    """Test creating multiple teams"""
    teams = [{"name": "Team A"}, {"name": "Team B"}]
    
    for team in teams:
        response = client.post("/teams", json=team)
        assert response.status_code == 200
    
    # Verify both teams exist
    response = client.get("/teams")
    assert response.status_code == 200
    team_list = response.json()
    assert len(team_list) == 2
    team_names = [t["name"] for t in team_list]
    assert "Team A" in team_names
    assert "Team B" in team_names
    
    # Verify event publishing was called twice
    assert mock_publish.call_count == 2