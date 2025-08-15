import zmq
import json
import logging
import threading
import time
from typing import Dict, Any
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import TournamentTeam

logger = logging.getLogger(__name__)

class EventSubscriber:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://team-service:5555")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
        self.running = False
        self.thread = None
        logger.info("ZeroMQ subscriber connected to tcp://team-service:5555")
    
    def start(self):
        """Start the subscriber in a background thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()
            logger.info("Event subscriber started")
    
    def stop(self):
        """Stop the subscriber"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.socket.close()
        self.context.term()
        logger.info("Event subscriber stopped")
    
    def _listen(self):
        """Listen for events in background thread"""
        while self.running:
            try:
                # Set a timeout to check if we should stop
                if self.socket.poll(1000):  # 1 second timeout
                    message = self.socket.recv_string(zmq.NOBLOCK)
                    self._handle_message(message)
            except zmq.Again:
                # No message received within timeout, continue
                continue
            except Exception as e:
                logger.error(f"Error receiving message: {str(e)}")
                time.sleep(1)
    
    def _handle_message(self, message: str):
        """Handle incoming message"""
        try:
            event = json.loads(message)
            logger.info(f"Received event: {event}")
            
            if event.get("event") == "TeamRegistered":
                self._handle_team_registered(event)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON message: {message}, error: {str(e)}")
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
    
    def _handle_team_registered(self, event: Dict[str, Any]):
        """Handle TeamRegistered event"""
        try:
            payload = event.get("payload", {})
            team_id = payload.get("teamId")
            team_name = payload.get("name")
            
            if not team_id or not team_name:
                logger.warning(f"Incomplete team data in event: {event}")
                return
            
            db = SessionLocal()
            try:
                # Create a tournament team record (demonstrating reaction to event)
                tournament_team = TournamentTeam(
                    tournament_id=1,  # Default tournament for demo
                    team_id=team_id,
                    team_name=team_name
                )
                
                db.add(tournament_team)
                db.commit()
                
                logger.info(f"Created tournament team entry for team: {team_name} (ID: {team_id})")
                
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to create tournament team entry: {str(e)}")
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error handling TeamRegistered event: {str(e)}")

# Global subscriber instance
_subscriber = None

def get_subscriber():
    global _subscriber
    if _subscriber is None:
        _subscriber = EventSubscriber()
    return _subscriber

def start_event_subscriber():
    """Start the event subscriber"""
    subscriber = get_subscriber()
    subscriber.start()

def stop_event_subscriber():
    """Stop the event subscriber"""
    global _subscriber
    if _subscriber:
        _subscriber.stop()
        _subscriber = None