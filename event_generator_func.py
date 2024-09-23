import json
import sqlite3
import random
import time
from uuid import uuid4
import requests
import asyncio
import httpx
# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('alchem.db')
    return conn


# Insert event into the database
def insert_event(event):
    event_name = event['event_name']
    event_data = json.dumps(event['event_data'])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO events (id, event_name, event_data) VALUES (?, ?, ?)
    """, (str(uuid4()),event_name, event_data))
    conn.commit()
    conn.close()

# post event to endpoint
async def post_event(event):
    print("Posting event")
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:80/event", json=event)
        return response


# Generate random event type and status
def generate_random_event():
    user_id = "69495b0c-a003-408a-bffe-a0b18f62d1d6"
    event_types = ['user_login', 'user_logout']
    statuses = ['started', 'completed', 'error']
    event_type = random.choice(event_types)
    status = random.choice(statuses)
    if (event_type == 'user_login' or event_type == 'user_logout'):
        event = {
            "event_name": event_type,
            "event_data": {
                "user_id": user_id,
                "status": status
            },
        }
        return event
    event = {
        "event_name": event_type,
        "event_data": {
            "status": status
        }
    }
    return event

async def generate_events() -> None:
    events = []
    for _ in range(10):
        event = generate_random_event()
        events.append(event)
        # insert_event(event)
        await post_event(event)
        print(f"Generated event: {event['event_name']} with status {event['event_data']['status']}")
        await asyncio.sleep(3)
    print("Event generation complete")
    with open("events.txt", "w") as file:
        json.dump(events, file) 


asyncio.run(generate_events())