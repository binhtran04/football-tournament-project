import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://team-service:5555")

topic = "teamServiceTopic"
socket.setsockopt_string(zmq.SUBSCRIBE, topic)

print(f"[tournament-service] Subscribing to topic: {topic}...")

while True:
    # Receive the full message
    message = socket.recv_string()
    
    # Parse out the topic and payload
    topic, payload = message.split(' ', 1)
    data = json.loads(payload)
    
    print(f"[tournament-service] Received event: {data}")