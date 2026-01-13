# --- Plan Endpoints ---
class PlanCreate(BaseModel):
    name: str
    description: str
    capacity: int

@app.post("/plans", status_code=201)
def create_plan(plan: PlanCreate, admin: Member = Depends(require_admin)):
    new_id = str(len(plans) + 1)
    new_plan = Plan(id=new_id, **plan.dict())
    plans[new_id] = new_plan
    return new_plan

@app.get("/plans")
def list_plans():
    return list(plans.values())

# --- Subscription Endpoints ---
class SubscriptionCreate(BaseModel):
    plan_id: str

@app.post("/subscriptions", status_code=201)
def create_subscription(sub: SubscriptionCreate, current: Member = Depends(get_current_member)):
    if sub.plan_id not in plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    # Check for existing subscription
    for s in subscriptions.values():
        if s.member_id == current.id and s.plan_id == sub.plan_id:
            raise HTTPException(status_code=400, detail="Already subscribed to this plan")
    new_id = str(len(subscriptions) + 1)
    new_sub = Subscription(id=new_id, member_id=current.id, plan_id=sub.plan_id, status="active")
    subscriptions[new_id] = new_sub
    return new_sub

@app.get("/subscriptions")
def list_subscriptions(status: Optional[str] = None, current: Member = Depends(get_current_member)):
    result = [s for s in subscriptions.values() if s.member_id == current.id]
    if status:
        result = [s for s in result if s.status == status]
    return result

# --- Notification Endpoint (stub) ---
class EmailNotification(BaseModel):
    to: str
    subject: str
    body: str

@app.post("/notifications/email")
def send_email_notification(notification: EmailNotification, admin: Member = Depends(require_admin)):
    # Stub: In production, send an actual email
    return {"status": "sent", "to": notification.to, "subject": notification.subject}
# --- Plan and Subscription Models ---
class Plan(BaseModel):
    id: str
    name: str
    description: str
    capacity: int

class Subscription(BaseModel):
    id: str
    member_id: str
    plan_id: str
    status: str  # active, expiring, expired

plans: Dict[str, Plan] = {
    "1": Plan(id="1", name="Standard", description="Standard club membership", capacity=100),
    "2": Plan(id="2", name="Premium", description="Premium club membership", capacity=20)
}

subscriptions: Dict[str, Subscription] = {}
"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from typing import Optional, Dict
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# --- In-memory member database and auth ---
SECRET_KEY = "supersecretkey"  # In production, use a secure key and env vars
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class Member(BaseModel):
    id: str
    email: str
    name: str
    role: str = "viewer"  # 'admin' or 'viewer'
    password: str  # Plaintext for demo only

members: Dict[str, Member] = {
    "1": Member(id="1", email="admin@mergington.edu", name="Admin User", role="admin", password="adminpass"),
    "2": Member(id="2", email="student@mergington.edu", name="Student User", role="viewer", password="studentpass")
}
email_to_id = {m.email: m.id for m in members.values()}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_member(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        member_id: str = payload.get("sub")
        if member_id is None or member_id not in members:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return members[member_id]

def require_admin(member: Member = Depends(get_current_member)):
    if member.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return member

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

 # In-memory activity database
activities = {

    # --- Member Endpoints ---
    class MemberCreate(BaseModel):
        email: str
        name: str
        password: str

    @app.post("/members", status_code=201)
    def create_member(member: MemberCreate):
        if member.email in email_to_id:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_id = str(len(members) + 1)
        new_member = Member(id=new_id, email=member.email, name=member.name, password=member.password)
        members[new_id] = new_member
        email_to_id[member.email] = new_id
        return {"id": new_id, "email": member.email, "name": member.name}

    @app.post("/auth/login")
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        user_id = email_to_id.get(form_data.username)
        if not user_id or members[user_id].password != form_data.password:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        access_token = create_access_token(data={"sub": user_id})
        return {"access_token": access_token, "token_type": "bearer"}

    @app.get("/members/{member_id}")
    def get_member_profile(member_id: str, current: Member = Depends(get_current_member)):
        if member_id != current.id and current.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this profile")
        member = members.get(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        return {"id": member.id, "email": member.email, "name": member.name, "role": member.role}
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
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities



# Updated: Sign up using member ID, require authentication
@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, current: Member = Depends(get_current_member)):
    """Sign up a member for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    email = current.email
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Member is already signed up")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}



# Updated: Unregister using member ID, require authentication
@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, current: Member = Depends(get_current_member)):
    """Unregister a member from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    email = current.email
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Member is not signed up for this activity")
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
