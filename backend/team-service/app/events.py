import zmq
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EventPublisher:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://0.0.0.0:5555")
        logger.info("ZeroMQ publisher bound to tcp://0.0.0.0:5555")
    
    def publish_team_registered(self, team_data: Dict[str, Any]):
        event = {
            "event": "TeamRegistered",
            "payload": {
                "teamId": team_data["team_id"],
                "name": team_data["name"]
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        message = json.dumps(event)
        self.socket.send_string(message)
        logger.info(f"Published TeamRegistered event: {event}")
    
    def close(self):
        self.socket.close()
        self.context.term()

# Global publisher instance
_publisher = None

def get_publisher():
    global _publisher
    if _publisher is None:
        _publisher = EventPublisher()
    return _publisher

def publish_team_registered(team_data: Dict[str, Any]):
    publisher = get_publisher()
    publisher.publish_team_registered(team_data)