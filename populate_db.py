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

# Sample teams data
teams = [
    {
        "name": "Mercedes",
        "year_founded": 1954,
        "total_pole_positions": 128,
        "total_race_wins": 115,
        "total_constructor_titles": 8,
        "finishing_position_previous_season": 2
    },
    {
        "name": "Red Bull Racing",
        "year_founded": 2005,
        "total_pole_positions": 92,
        "total_race_wins": 107,
        "total_constructor_titles": 6,
        "finishing_position_previous_season": 1
    },
    {
        "name": "Ferrari",
        "year_founded": 1950,
        "total_pole_positions": 242,
        "total_race_wins": 243,
        "total_constructor_titles": 16,
        "finishing_position_previous_season": 3
    },
    {
        "name": "McLaren",
        "year_founded": 1966,
        "total_pole_positions": 156,
        "total_race_wins": 183,
        "total_constructor_titles": 8,
        "finishing_position_previous_season": 4
    },
    {
        "name": "Aston Martin",
        "year_founded": 2021,
        "total_pole_positions": 1,
        "total_race_wins": 0,
        "total_constructor_titles": 0,
        "finishing_position_previous_season": 5
    }
]

# Sample drivers data
drivers = [
    {
        "name": "Lewis Hamilton",
        "age": 39,
        "team": "Mercedes",
        "total_pole_positions": 104,
        "total_race_wins": 103,
        "total_points_scored": 4639.5,
        "total_world_titles": 7,
        "total_fastest_laps": 64
    },
    {
        "name": "Max Verstappen",
        "age": 26,
        "team": "Red Bull Racing",
        "total_pole_positions": 39,
        "total_race_wins": 56,
        "total_points_scored": 2586.5,
        "total_world_titles": 3,
        "total_fastest_laps": 30
    },
    {
        "name": "Charles Leclerc",
        "age": 26,
        "team": "Ferrari",
        "total_pole_positions": 23,
        "total_race_wins": 5,
        "total_points_scored": 1074,
        "total_world_titles": 0,
        "total_fastest_laps": 7
    },
    {
        "name": "Lando Norris",
        "age": 24,
        "team": "McLaren",
        "total_pole_positions": 3,
        "total_race_wins": 2,
        "total_points_scored": 696,
        "total_world_titles": 0,
        "total_fastest_laps": 8
    },
    {
        "name": "Fernando Alonso",
        "age": 42,
        "team": "Aston Martin",
        "total_pole_positions": 22,
        "total_race_wins": 32,
        "total_points_scored": 2267,
        "total_world_titles": 2,
        "total_fastest_laps": 24
    },
    {
        "name": "George Russell",
        "age": 26,
        "team": "Mercedes",
        "total_pole_positions": 3,
        "total_race_wins": 2,
        "total_points_scored": 452,
        "total_world_titles": 0,
        "total_fastest_laps": 6
    },
    {
        "name": "Carlos Sainz",
        "age": 29,
        "team": "Ferrari",
        "total_pole_positions": 5,
        "total_race_wins": 3,
        "total_points_scored": 967.5,
        "total_world_titles": 0,
        "total_fastest_laps": 3
    }
]

def populate_teams():
    """Add sample teams to Firestore"""
    teams_collection = db.collection('teams')
    
    # Check if teams already exist
    existing_teams = [doc.to_dict().get('name') for doc in teams_collection.stream()]
    
    for team in teams:
        if team['name'] not in existing_teams:
            print(f"Adding team: {team['name']}")
            teams_collection.add(team)
        else:
            print(f"Team {team['name']} already exists, skipping")
    
    print("Teams population complete!")

def populate_drivers():
    """Add sample drivers to Firestore"""
    drivers_collection = db.collection('drivers')
    
    # Check if drivers already exist
    existing_drivers = [doc.to_dict().get('name') for doc in drivers_collection.stream()]
    
    for driver in drivers:
        if driver['name'] not in existing_drivers:
            print(f"Adding driver: {driver['name']}")
            drivers_collection.add(driver)
        else:
            print(f"Driver {driver['name']} already exists, skipping")
    
    print("Drivers population complete!")

if __name__ == "__main__":
    print("Starting database population...")
    
    # First add teams, then drivers (since drivers reference teams)
    populate_teams()
    time.sleep(1)  # Small delay to ensure teams are fully written
    populate_drivers()
    
    print("Database population complete!") 