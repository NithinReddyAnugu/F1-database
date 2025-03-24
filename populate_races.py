import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import time

# Initialize Firebase Admin SDK
try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("f1formula-f6f18-firebase-adminsdk-fbsvc-89d270ff8f.json")
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Sample races data for 2023 season
races_2023 = [
    {
        "name": "Bahrain Grand Prix",
        "circuit": "Bahrain International Circuit",
        "date": datetime.datetime(2023, 3, 5),
        "season": 2023,
        "results": [
            {
                "driver": "Max Verstappen",
                "position": 1,
                "points": 25,
                "fastest_lap": False
            },
            {
                "driver": "Sergio Perez",
                "position": 2,
                "points": 18,
                "fastest_lap": False
            },
            {
                "driver": "Fernando Alonso",
                "position": 3,
                "points": 15,
                "fastest_lap": False
            },
            {
                "driver": "Lewis Hamilton",
                "position": 5,
                "points": 10,
                "fastest_lap": True
            }
        ]
    },
    {
        "name": "Saudi Arabian Grand Prix",
        "circuit": "Jeddah Corniche Circuit",
        "date": datetime.datetime(2023, 3, 19),
        "season": 2023,
        "results": [
            {
                "driver": "Sergio Perez",
                "position": 1,
                "points": 25,
                "fastest_lap": False
            },
            {
                "driver": "Max Verstappen",
                "position": 2,
                "points": 19,
                "fastest_lap": True
            },
            {
                "driver": "Fernando Alonso",
                "position": 3,
                "points": 15,
                "fastest_lap": False
            }
        ]
    },
    {
        "name": "Australian Grand Prix",
        "circuit": "Albert Park Circuit",
        "date": datetime.datetime(2023, 4, 2),
        "season": 2023,
        "results": [
            {
                "driver": "Max Verstappen",
                "position": 1,
                "points": 25,
                "fastest_lap": False
            },
            {
                "driver": "Lewis Hamilton",
                "position": 2,
                "points": 18,
                "fastest_lap": False
            },
            {
                "driver": "Fernando Alonso",
                "position": 3,
                "points": 15,
                "fastest_lap": False
            },
            {
                "driver": "Charles Leclerc",
                "position": 7,
                "points": 7,
                "fastest_lap": True
            }
        ]
    }
]

# Sample races data for 2024 season
races_2024 = [
    {
        "name": "Bahrain Grand Prix",
        "circuit": "Bahrain International Circuit",
        "date": datetime.datetime(2024, 3, 2),
        "season": 2024,
        "results": [
            {
                "driver": "Max Verstappen",
                "position": 1,
                "points": 25,
                "fastest_lap": False
            },
            {
                "driver": "Carlos Sainz",
                "position": 2,
                "points": 18,
                "fastest_lap": False
            },
            {
                "driver": "Charles Leclerc",
                "position": 3,
                "points": 15,
                "fastest_lap": False
            },
            {
                "driver": "Lewis Hamilton",
                "position": 7,
                "points": 7,
                "fastest_lap": True
            }
        ]
    },
    {
        "name": "Saudi Arabian Grand Prix",
        "circuit": "Jeddah Corniche Circuit",
        "date": datetime.datetime(2024, 3, 9),
        "season": 2024,
        "results": [
            {
                "driver": "Max Verstappen",
                "position": 1,
                "points": 25,
                "fastest_lap": False
            },
            {
                "driver": "Charles Leclerc",
                "position": 2,
                "points": 19,
                "fastest_lap": True
            },
            {
                "driver": "Carlos Sainz",
                "position": 3,
                "points": 15,
                "fastest_lap": False
            }
        ]
    }
]

def populate_races():
    """Add sample races to Firestore"""
    races_collection = db.collection('races')
    
    # Combine all races
    all_races = races_2023 + races_2024
    
    # Check for existing races to avoid duplicates
    existing_races = []
    for doc in races_collection.stream():
        race_data = doc.to_dict()
        if "name" in race_data and "date" in race_data:
            existing_races.append(f"{race_data['name']}_{race_data['date'].strftime('%Y-%m-%d')}")
    
    # Add races that don't already exist
    for race in all_races:
        race_key = f"{race['name']}_{race['date'].strftime('%Y-%m-%d')}"
        if race_key not in existing_races:
            print(f"Adding race: {race['name']} ({race['date'].strftime('%Y-%m-%d')})")
            races_collection.add(race)
        else:
            print(f"Race {race['name']} ({race['date'].strftime('%Y-%m-%d')}) already exists, skipping")
    
    print("Races population complete!")

if __name__ == "__main__":
    print("Starting races population...")
    populate_races()
    print("Database population complete!") 