from datetime import datetime, timedelta

def get_mock_users():
    return [
        {
            "id": "user1",
            "name": "Sarah Johnson",
            "email": "sarah@safecircle.com",
            "phone": "+1 555-0101",
            "profilePic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah",
            "bio": "Computer Science student, always ready to help",
            "profileComplete": True,
            "level": 3,
            "points": 450,
            "responses": 12,
            "rating": 4.8,
            "badges": ["first-responder", "speed-demon", "guardian-angel"],
            "bloodType": "O+",
            "allergies": "Penicillin, Peanuts",
            "medications": "Insulin, EpiPen",
            "medicalConditions": "Type 1 Diabetes",
            "emergencyContacts": [
                { "name": "Emergency Contact", "relationship": "Primary", "phone": "+91 9675852627" },
                { "name": "Mom", "relationship": "Mother", "phone": "+1 555-1234" }
            ],
            "trustedCircle": ["user2", "user3", "user4"],
            "preferences": {
                "receiveAlerts": { "medical": True, "assault": True, "accident": True, "other": True },
                "alertRadius": 1000,
                "silentMode": False
            }
        },
        {
            "id": "user2",
            "name": "Mike Chen",
            "email": "mike@safecircle.com",
            "phone": "+1 555-0102",
            "profilePic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mike",
            "bio": "Pre-med student with first aid certification",
            "profileComplete": True,
            "level": 4,
            "points": 680,
            "responses": 20,
            "rating": 4.9,
            "badges": ["first-responder", "speed-demon", "lifesaver", "certified-helper"],
            "bloodType": "A+",
            "allergies": "None",
            "medications": "None",
            "medicalConditions": "None",
            "emergencyContacts": [
                { "name": "Emily Chen", "relationship": "Sister", "phone": "+1 555-2234" }
            ],
            "trustedCircle": ["user1", "user5"],
            "preferences": {
                "receiveAlerts": { "medical": True, "assault": True, "accident": True, "other": True },
                "alertRadius": 1500,
                "silentMode": False
            }
        },
        {
            "id": "user3",
            "name": "Emma Wilson",
            "email": "emma@safecircle.com",
            "phone": "+1 555-0103",
            "profilePic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emma",
            "bio": "Psychology major, mental health advocate",
            "profileComplete": True,
            "level": 2,
            "points": 280,
            "responses": 8,
            "rating": 4.7,
            "badges": ["first-responder", "guardian-angel"],
            "bloodType": "B+",
            "allergies": "Latex",
            "medications": "None",
            "medicalConditions": "None",
            "emergencyContacts": [
                { "name": "Mom", "relationship": "Mother", "phone": "+1 555-3234" }
            ],
            "trustedCircle": ["user1", "user2"],
            "preferences": {
                "receiveAlerts": { "medical": True, "assault": True, "accident": False, "other": True },
                "alertRadius": 800,
                "silentMode": False
            }
        },
        {
            "id": "user4",
            "name": "James Rodriguez",
            "email": "james@safecircle.com",
            "phone": "+1 555-0104",
            "profilePic": "https://api.dicebear.com/7.x/avataaars/svg?seed=James",
            "bio": "Engineering student, campus security volunteer",
            "profileComplete": True,
            "level": 5,
            "points": 1250,
            "responses": 35,
            "rating": 4.9,
            "badges": ["first-responder", "speed-demon", "lifesaver", "community-hero", "night-watch", "legend"],
            "bloodType": "AB+",
            "allergies": "None",
            "medications": "None",
            "medicalConditions": "None",
            "emergencyContacts": [
                { "name": "Maria Rodriguez", "relationship": "Mother", "phone": "+1 555-4234" }
            ],
            "trustedCircle": ["user1", "user5"],
            "preferences": {
                "receiveAlerts": { "medical": True, "assault": True, "accident": True, "other": True },
                "alertRadius": 2000,
                "silentMode": False
            }
        },
        {
            "id": "user5",
            "name": "Lily Park",
            "email": "lily@safecircle.com",
            "phone": "+1 555-0105",
            "profilePic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Lily",
            "bio": "Nursing student, certified EMT",
            "profileComplete": True,
            "level": 4,
            "points": 920,
            "responses": 28,
            "rating": 5.0,
            "badges": ["first-responder", "speed-demon", "lifesaver", "certified-helper", "accuracy-expert"],
            "bloodType": "O-",
            "allergies": "None",
            "medications": "None",
            "medicalConditions": "None",
            "emergencyContacts": [
                { "name": "David Park", "relationship": "Father", "phone": "+1 555-5234" }
            ],
            "trustedCircle": ["user2", "user4"],
            "preferences": {
                "receiveAlerts": { "medical": True, "assault": True, "accident": True, "other": True },
                "alertRadius": 1500,
                "silentMode": False
            }
        }
    ]

def get_mock_incidents(users):
    now = datetime.now()
    return [
        {
            "id": "incident1",
            "type": "Medical",
            "victim": users[0],
            "location": { "lat": 37.7749, "lng": -122.4194, "address": "Main Library, Campus" },
            "distance": 350,
            "description": "Feeling dizzy and disoriented",
            "timestamp": (now - timedelta(minutes=3)).isoformat(),
            "status": "active",
            "respondingHelpers": ["user2", "user4", "user5"],
            "arrivedHelpers": [],
            "emergencyServicesNotified": ["campus-security", "ambulance"],
            "chatMessages": [
                { "id": "msg1", "sender": "user2", "message": "I'm 2 minutes away with first aid kit", "timestamp": (now - timedelta(minutes=2)).isoformat() },
                { "id": "msg2", "sender": "user1", "message": "I'm at the library near the entrance", "timestamp": (now - timedelta(minutes=1.5)).isoformat() },
                { "id": "msg3", "sender": "user4", "message": "Campus security has been notified", "timestamp": (now - timedelta(minutes=1)).isoformat() }
            ]
        },
        {
            "id": "incident2",
            "type": "Assault",
            "victim": users[2],
            "location": { "lat": 37.7739, "lng": -122.4200, "address": "North Parking Lot" },
            "distance": 580,
            "description": "Feeling unsafe, someone following me",
            "timestamp": (now - timedelta(minutes=5)).isoformat(),
            "status": "active",
            "respondingHelpers": ["user4"],
            "arrivedHelpers": [],
            "emergencyServicesNotified": ["campus-security", "police"],
            "chatMessages": [
                { "id": "msg4", "sender": "user4", "message": "On my way, stay in well-lit area", "timestamp": (now - timedelta(minutes=3)).isoformat() },
                { "id": "msg5", "sender": "user3", "message": "I'm near the campus store, moving towards the lot entrance", "timestamp": (now - timedelta(minutes=2)).isoformat() }
            ]
        },
        {
            "id": "incident3",
            "type": "Accident",
            "victim": users[1],
            "location": { "lat": 37.7759, "lng": -122.4184, "address": "Sports Complex" },
            "distance": 920,
            "description": "Twisted ankle during basketball",
            "timestamp": (now - timedelta(minutes=8)).isoformat(),
            "status": "active",
            "respondingHelpers": ["user5"],
            "arrivedHelpers": ["user5"],
            "emergencyServicesNotified": ["campus-security"],
            "chatMessages": [
                { "id": "msg6", "sender": "user5", "message": "I'm here with ice pack and compression wrap", "timestamp": (now - timedelta(minutes=1)).isoformat() }
            ]
        }
    ]
