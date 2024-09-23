from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from typing import Any
import sqlite3
from pydantic import BaseModel
import json

DB_PATH = "./alchem.db"

class Event(BaseModel):
    event_name: str
    event_data: Any


def create_table():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS events (CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, id TEXT PRIMARY KEY, event_name TEXT, event_data JSON)")
    cur.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, username TEXT, password TEXT, logged_in BOOLEAN)")
    cur.execute("INSERT INTO users (id, username, password, logged_in) VALUES (?, ?, ?, ?) ON CONFLICT(id) DO NOTHING", ("69495b0c-a003-408a-bffe-a0b18f62d1d6", "admin", "admin", False))
    con.commit()
    con.close()

# acting as the functional layer
def process_event(event: Event):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO events (id, event_name, event_data) VALUES (?, ?, ?)", (str(uuid4()), event.event_name, json.dumps(event.event_data)))
    con.commit()
    con.close()
    print(f"Received event: {event.event_name} with data {event.event_data}")
    if event.event_name == "user_login":
        print(f"User {event.event_data["user_id"]} logged in")
    elif event.event_name == "user_logout":
        print(f"User {event.event_data["user_id"]} logged out")
    return

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(lifespan=lifespan, debug=True)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.get("/")
def hello_world(background_tasks: BackgroundTasks):
    return {
        "status": 200,
        "body": "Alchem API"
    }

# writes the event to the database
@app.post("/event")
async def event(event: Event, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_event, event)
    return {
        "status": 200,
        "body": "Event received"
    }

# reads all events from the database
@app.get("/events")
async def events():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM events ORDER BY CREATED_AT DESC")
    rows = cur.fetchall()
    con.close()
    return {
        "status": 200,
        "body": rows
    }

@app.get("/latest_event_id")
async def latest_event_id():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM events ORDER BY CREATED_AT DESC LIMIT 1")
    row = cur.fetchone()
    con.close()
    if row is None:
        return {
            "status": 200,
            "id": None
        }
    return {
        "status": 200,
        "id": row[0]
    }