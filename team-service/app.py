import time
import zmq
import json
import uuid

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

topic = "teamServiceTopic"
print(f"[team-service] Publishing events to topic: {topic}...")

while True:
    team_id = str(uuid.uuid4())
    team_name = "Oulu FC"
    event = {
      "event": "team.registered",
      "team_id": team_id,
      "name": team_name,
    }
    # Publish with topic prefix
    socket.send_string(f"{topic} {json.dumps(event)}")
    print(f"[team-service] Published event: {event['event']} with team_id: {team_id} "+
      f"and name: {team_name}")
    time.sleep(3)