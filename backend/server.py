from fastapi import FastAPI, APIRouter, HTTPException, Body
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from seed import get_mock_users, get_mock_incidents
from mock_db import MockClient

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
try:
    # Try to connect to real MongoDB if available, otherwise use Mock
    # Since AsyncIOMotorClient is lazy, we can't easily check here.
    # For this environment, we'll default to MockClient to ensure it works without external dependencies.
    # To use real MongoDB, uncomment the following lines and comment out MockClient:
    # client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
    
    logger = logging.getLogger("uvicorn")
    logger.info("Using In-Memory Mock Database (data will reset on restart)")
    client = MockClient(mongo_url)
except Exception as e:
    print(f"Error initializing DB client: {e}")
    client = MockClient(mongo_url)

db_name = os.environ.get('DB_NAME', 'safecircle')
db = client[db_name]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    profilePic: Optional[str] = None
    bio: Optional[str] = None
    profileComplete: bool = False
    level: int = 1
    points: int = 0
    responses: int = 0
    rating: float = 0.0
    badges: List[str] = []
    bloodType: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    medicalConditions: Optional[str] = None
    emergencyContacts: List[Dict[str, str]] = []
    trustedCircle: List[str] = []
    preferences: Dict[str, Any] = {}
    createdAt: Optional[str] = None
    location: Optional[Dict[str, Any]] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class Incident(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    type: str
    victim: User
    location: Dict[str, Any]
    distance: Optional[float] = None
    description: Optional[str] = None
    timestamp: str
    status: str
    respondingHelpers: List[str] = []
    arrivedHelpers: List[str] = []
    emergencyServicesNotified: List[str] = []
    chatMessages: List[Dict[str, Any]] = []

# Routes
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

class LocationUpdate(BaseModel):
    lat: float
    lng: float
    address: Optional[str] = None

@api_router.put("/users/{user_id}/location")
async def update_user_location(user_id: str, location: LocationUpdate):
    await db.users.update_one(
        {"id": user_id},
        {"$set": {"location": location.model_dump()}}
    )
    return {"status": "success"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks

# User Routes
@api_router.get("/users", response_model=List[User])
async def get_users():
    users = await db.users.find({}, {"_id": 0}).to_list(1000)
    return users

@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@api_router.post("/login", response_model=User)
async def login(login_data: LoginRequest):
    user = await db.users.find_one({"email": login_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@api_router.post("/users", response_model=User)
async def create_user(user: User):
    await db.users.insert_one(user.model_dump())
    return user

@api_router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: Dict[str, Any] = Body(...)):
    result = await db.users.update_one({"id": user_id}, {"$set": user_update})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    updated_user = await db.users.find_one({"id": user_id}, {"_id": 0})
    return updated_user

# Incident Routes
@api_router.get("/incidents", response_model=List[Incident])
async def get_incidents():
    incidents = await db.incidents.find({}, {"_id": 0}).to_list(1000)
    return incidents

@api_router.post("/incidents", response_model=Incident)
async def create_incident(incident: Incident):
    # Save incident to database
    await db.incidents.insert_one(incident.model_dump())
    
    # Notify Emergency Contacts (Server-Side Automation)
    try:
        victim = incident.victim
        if victim and victim.emergencyContacts:
            for contact in victim.emergencyContacts:
                if contact.phone:
                    # Construct Message
                    location_url = f"https://www.google.com/maps?q={incident.location.lat},{incident.location.lng}"
                    message = f"SOS ALERT! {victim.name} needs help. Type: {incident.type}. Location: {location_url}"
                    
                    # 1. Log to Console (Simulation)
                    print(f"\n[SERVER-SIDE-NOTIFICATION] Sending SMS/WhatsApp to {contact.name} ({contact.phone}):")
                    print(f"Message: {message}\n")
                    
                    # 2. Twilio Integration (Uncomment and add credentials to .env to enable real sending)
                    # from twilio.rest import Client
                    # import os
                    # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
                    # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
                    # from_number = os.getenv('TWILIO_PHONE_NUMBER')
                    # if account_sid and auth_token and from_number:
                    #     client = Client(account_sid, auth_token)
                    #     client.messages.create(body=message, from_=from_number, to=contact.phone)

    except Exception as e:
        print(f"Error sending notifications: {e}")

    return incident

@api_router.get("/incidents/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    incident = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

# Leaderboard Route
@api_router.get("/leaderboard")
async def get_leaderboard():
    users = await db.users.find({}, {"_id": 0}).sort("points", -1).limit(10).to_list(10)
    leaderboard = []
    for i, user in enumerate(users):
        leaderboard.append({
            "rank": i + 1,
            "user": user,
            "points": user.get("points", 0),
            "responses": user.get("responses", 0),
            "change": "0" # Placeholder logic for change
        })
    return leaderboard

# Include the router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"], # Allow all for now to ensure connectivity
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Seed Data on Startup
@app.on_event("startup")
async def startup_db_client():
    try:
        # Check if users exist
        if await db.users.count_documents({}) == 0:
            logger.info("Seeding users...")
            mock_users = get_mock_users()
            await db.users.insert_many(mock_users)
            
            # Check if incidents exist (only seed if users were seeded to ensure consistency)
            if await db.incidents.count_documents({}) == 0:
                logger.info("Seeding incidents...")
                mock_incidents = get_mock_incidents(mock_users)
                await db.incidents.insert_many(mock_incidents)
    except Exception as e:
        logger.error(f"Error seeding database: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
