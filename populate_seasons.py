import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase Admin SDK
try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("f1formula-f6f18-firebase-adminsdk-fbsvc-89d270ff8f.json")
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Sample seasons data
seasons = [
    {
        "year": 2020,
        "driver_champion": "Lewis Hamilton",
        "team_champion": "Mercedes",
        "total_races": 17,
        "notable_events": [
            "Season delayed and shortened due to COVID-19 pandemic",
            "Lewis Hamilton equaled Michael Schumacher's record of 7 world championships",
            "Racing Point controversially copied Mercedes' 2019 car design"
        ]
    },
    {
        "year": 2021,
        "driver_champion": "Max Verstappen",
        "team_champion": "Mercedes",
        "total_races": 22,
        "notable_events": [
            "Controversial season finale at Abu Dhabi Grand Prix",
            "Max Verstappen won his first world championship on the last lap of the season",
            "Introduction of sprint races at select events"
        ]
    },
    {
        "year": 2022,
        "driver_champion": "Max Verstappen",
        "team_champion": "Red Bull Racing",
        "total_races": 22,
        "notable_events": [
            "New technical regulations introduced major car design changes",
            "Ferrari started strong but fell behind in development race",
            "Max Verstappen dominated with 15 race wins in a single season"
        ]
    },
    {
        "year": 2023,
        "driver_champion": "Max Verstappen",
        "team_champion": "Red Bull Racing",
        "total_races": 22,
        "notable_events": [
            "Red Bull won 21 of 22 races",
            "Max Verstappen set record with 19 race wins in a single season",
            "McLaren made significant mid-season improvements"
        ]
    }
]

def populate_seasons():
    """Add sample seasons to Firestore"""
    seasons_collection = db.collection('seasons')
    
    # Check if seasons already exist
    existing_seasons = [doc.to_dict().get('year') for doc in seasons_collection.stream()]
    
    for season in seasons:
        if season['year'] not in existing_seasons:
            print(f"Adding season: {season['year']}")
            seasons_collection.add(season)
        else:
            print(f"Season {season['year']} already exists, skipping")
    
    print("Seasons population complete!")

if __name__ == "__main__":
    print("Starting seasons database population...")
    
    populate_seasons()
    
    print("Seasons database population complete!") 