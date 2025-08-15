import zmq
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EventPublisher:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        # Set high water mark to prevent message loss
        self.socket.set_hwm(1000)
        # Set linger time to ensure messages are sent
        self.socket.set(zmq.LINGER, 1000)
        self.socket.bind("tcp://0.0.0.0:5555")
        logger.info("ZeroMQ publisher bound to tcp://0.0.0.0:5555")
        # Give ZeroMQ time to establish connections (important for slow joiners)
        time.sleep(0.5)
        self._initialized = True
    
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
        # Small delay to ensure slow joiners can receive the message
        time.sleep(0.01)
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
        logger.info("Creating new ZeroMQ publisher instance")
        _publisher = EventPublisher()
    else:
        logger.debug("Using existing ZeroMQ publisher instance")
    return _publisher

def publish_team_registered(team_data: Dict[str, Any]):
    publisher = get_publisher()
    publisher.publish_team_registered(team_data)