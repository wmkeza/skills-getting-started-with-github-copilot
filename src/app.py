"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all available activities"""
    # Adding more activities
    activities["Soccer Team"] = {
        "description": "Competitive soccer team with weekly matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "james@mergington.edu"]
    }
    
    activities["Swimming Club"] = {
        "description": "Swimming practice and competitions",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["natalie@mergington.edu"]
    }
    
    activities["Art Workshop"] = {
        "description": "Learn different art techniques and create artwork",
        "schedule": "Mondays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["emily@mergington.edu"]
    }
    
    activities["Drama Club"] = {
        "description": "Theater performances and acting workshops",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    }
    
    activities["Science Olympiad"] = {
        "description": "Prepare for and compete in science competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["zoe@mergington.edu"]
    }
    
    activities["Debate Team"] = {
        "description": "Learn debating skills and participate in tournaments",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["ethan@mergington.edu", "liam@mergington.edu"]
    }
    
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specificy activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
