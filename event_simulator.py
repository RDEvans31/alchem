import json
import time
import requests

print("Generating events")
with open('events.txt', 'r') as file:
    events = json.load(file)

# loop through the events and post them to the endpoint
for event in events:
    response = requests.post("http://localhost:80/event", json=event)
    print(f"Posted event: {event['event_name']} with status {event['event_data']['status']}")
    print(response.json())
    time.sleep(4)