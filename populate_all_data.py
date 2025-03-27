import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import time
import os
import logging
import json
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('F1-Database-Populator')

# Global variables for in-memory database (fallback)
in_memory_db = {
    'teams': [],
    'drivers': [],
    'seasons': [],
    'races': []
}
use_in_memory = False

def initialize_firebase():
    """Initialize Firebase with better error handling"""
    global use_in_memory
    
    # Check if we should use in-memory database instead
    if '--in-memory' in sys.argv:
        logger.info("Using in-memory database (Firebase bypass)")
        use_in_memory = True
        return None
    
    try:
        # Try to get the existing app first
        app = firebase_admin.get_app()
        logger.info("Firebase app already initialized")
        return firestore.client()
    except ValueError:
        # App not initialized yet
        logger.info("Initializing Firebase app")
        
        # Try the correct service account file names in order of preference
        potential_credential_files = [
            "f1formula-f6f18-firebase-adminsdk-fbsvc-74edc3c8b3.json",  # New correct file
            "firebase-credentials.json",  # Generic name
        ]
        
        # Find the first valid credential file
        cred_path = None
        for file_path in potential_credential_files:
            if os.path.exists(file_path):
                logger.info(f"Found credential file: {file_path}")
                cred_path = file_path
                break
        
        if not cred_path:
            logger.error("No valid Firebase credential file found")
            logger.warning("Switching to in-memory database mode")
            use_in_memory = True
            return None
        
        # Try to validate the JSON file
        try:
            with open(cred_path, 'r') as f:
                json_content = json.load(f)  # Will raise an exception if not valid JSON
                
                # Basic validation of service account file
                required_fields = ["type", "project_id", "private_key_id", "private_key", "client_email"]
                for field in required_fields:
                    if field not in json_content:
                        logger.error(f"Firebase credential file missing required field: {field}")
                        raise ValueError(f"Invalid service account file: missing {field}")
                
            # Initialize Firebase
            logger.info(f"Initializing Firebase with credentials from {cred_path}")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            
            # Test the connection
            db = firestore.client()
            # Try a simple operation to verify the connection
            db.collection('_test').document('_test').get()
            
            logger.info("Firebase initialized successfully and connection verified")
            return db
            
        except json.JSONDecodeError:
            logger.error(f"Credentials file is not valid JSON: {cred_path}")
            logger.warning("Switching to in-memory database mode")
            use_in_memory = True
            return None
        except ValueError as e:
            logger.error(f"Firebase credential validation error: {str(e)}")
            logger.warning("Switching to in-memory database mode")
            use_in_memory = True
            return None
        except Exception as e:
            logger.error(f"Error initializing Firebase: {str(e)}")
            logger.warning("Switching to in-memory database mode")
            use_in_memory = True
            return None

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
    },
    {
        "name": "Alpine",
        "year_founded": 2021,
        "total_pole_positions": 0,
        "total_race_wins": 1,
        "total_constructor_titles": 0,
        "finishing_position_previous_season": 6
    },
    {
        "name": "Williams",
        "year_founded": 1977,
        "total_pole_positions": 128,
        "total_race_wins": 114,
        "total_constructor_titles": 9,
        "finishing_position_previous_season": 7
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
    },
    {
        "name": "Sergio Perez",
        "age": 34,
        "team": "Red Bull Racing",
        "total_pole_positions": 4,
        "total_race_wins": 6,
        "total_points_scored": 1356,
        "total_world_titles": 0,
        "total_fastest_laps": 10
    },
    {
        "name": "Oscar Piastri",
        "age": 22,
        "team": "McLaren",
        "total_pole_positions": 1,
        "total_race_wins": 1,
        "total_points_scored": 180,
        "total_world_titles": 0,
        "total_fastest_laps": 2
    }
]

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
    },
    {
        "year": 2024,
        "driver_champion": "In progress",
        "team_champion": "In progress",
        "total_races": 24,
        "notable_events": [
            "Record-breaking 24-race calendar",
            "Six sprint races scheduled",
            "Added Las Vegas Grand Prix as a new event"
        ]
    }
]

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
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Sergio Perez",
                "position": 2,
                "points": 18,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Fernando Alonso",
                "position": 3,
                "points": 15,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Lewis Hamilton",
                "position": 5,
                "points": 10,
                "fastest_lap": True,
                "dnf": False
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
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Max Verstappen",
                "position": 2,
                "points": 19,
                "fastest_lap": True,
                "dnf": False
            },
            {
                "driver": "Fernando Alonso",
                "position": 3,
                "points": 15,
                "fastest_lap": False,
                "dnf": False
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
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Carlos Sainz",
                "position": 2,
                "points": 18,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Charles Leclerc",
                "position": 3,
                "points": 15,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Lewis Hamilton",
                "position": 7,
                "points": 7,
                "fastest_lap": True,
                "dnf": False
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
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Charles Leclerc",
                "position": 2,
                "points": 19,
                "fastest_lap": True,
                "dnf": False
            },
            {
                "driver": "Carlos Sainz",
                "position": 3,
                "points": 15,
                "fastest_lap": False,
                "dnf": False
            }
        ]
    },
    {
        "name": "Australian Grand Prix",
        "circuit": "Albert Park Circuit",
        "date": datetime.datetime(2024, 3, 24),
        "season": 2024,
        "results": [
            {
                "driver": "Carlos Sainz",
                "position": 1,
                "points": 25,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Charles Leclerc",
                "position": 2,
                "points": 18,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Lando Norris",
                "position": 3,
                "points": 15,
                "fastest_lap": False,
                "dnf": False
            },
            {
                "driver": "Max Verstappen",
                "position": 0,
                "points": 0,
                "fastest_lap": False,
                "dnf": True
            }
        ]
    }
]

def populate_teams(db):
    """Add sample teams to Firestore or in-memory database"""
    global in_memory_db
    added_count = 0
    skipped_count = 0
    
    if use_in_memory:
        # In-memory version
        existing_teams = [team["name"] for team in in_memory_db["teams"]]
        
        for team in teams:
            if team['name'] not in existing_teams:
                logger.info(f"Adding team (in-memory): {team['name']}")
                team_copy = team.copy()
                team_copy['id'] = str(hash(team['name']))  # Simple ID generation
                in_memory_db["teams"].append(team_copy)
                added_count += 1
            else:
                logger.info(f"Team (in-memory) {team['name']} already exists, skipping")
                skipped_count += 1
    else:
        # Firestore version
        teams_collection = db.collection('teams')
        
        # Check if teams already exist
        existing_teams = [doc.to_dict().get('name') for doc in teams_collection.stream()]
        
        for team in teams:
            if team['name'] not in existing_teams:
                try:
                    logger.info(f"Adding team: {team['name']}")
                    teams_collection.add(team)
                    added_count += 1
                except Exception as e:
                    logger.error(f"Error adding team {team['name']}: {str(e)}")
            else:
                logger.info(f"Team {team['name']} already exists, skipping")
                skipped_count += 1
    
    logger.info(f"Teams population complete! Added: {added_count}, Skipped: {skipped_count}")
    return added_count, skipped_count

def populate_drivers(db):
    """Add sample drivers to Firestore or in-memory database"""
    global in_memory_db
    added_count = 0
    skipped_count = 0
    
    if use_in_memory:
        # In-memory version
        existing_drivers = [driver["name"] for driver in in_memory_db["drivers"]]
        
        for driver in drivers:
            if driver['name'] not in existing_drivers:
                logger.info(f"Adding driver (in-memory): {driver['name']}")
                driver_copy = driver.copy()
                driver_copy['id'] = str(hash(driver['name']))  # Simple ID generation
                in_memory_db["drivers"].append(driver_copy)
                added_count += 1
            else:
                logger.info(f"Driver (in-memory) {driver['name']} already exists, skipping")
                skipped_count += 1
    else:
        # Firestore version
        drivers_collection = db.collection('drivers')
        
        # Check if drivers already exist
        existing_drivers = [doc.to_dict().get('name') for doc in drivers_collection.stream()]
        
        for driver in drivers:
            if driver['name'] not in existing_drivers:
                try:
                    logger.info(f"Adding driver: {driver['name']}")
                    drivers_collection.add(driver)
                    added_count += 1
                except Exception as e:
                    logger.error(f"Error adding driver {driver['name']}: {str(e)}")
            else:
                logger.info(f"Driver {driver['name']} already exists, skipping")
                skipped_count += 1
    
    logger.info(f"Drivers population complete! Added: {added_count}, Skipped: {skipped_count}")
    return added_count, skipped_count

def populate_seasons(db):
    """Add sample seasons to Firestore or in-memory database"""
    global in_memory_db
    added_count = 0
    skipped_count = 0
    
    if use_in_memory:
        # In-memory version
        existing_seasons = [season["year"] for season in in_memory_db["seasons"]]
        
        for season in seasons:
            if season['year'] not in existing_seasons:
                logger.info(f"Adding season (in-memory): {season['year']}")
                season_copy = season.copy()
                season_copy['id'] = str(season['year'])  # Use year as ID
                in_memory_db["seasons"].append(season_copy)
                added_count += 1
            else:
                logger.info(f"Season (in-memory) {season['year']} already exists, skipping")
                skipped_count += 1
    else:
        # Firestore version
        seasons_collection = db.collection('seasons')
        
        # Check if seasons already exist
        existing_seasons = [doc.to_dict().get('year') for doc in seasons_collection.stream()]
        
        for season in seasons:
            if season['year'] not in existing_seasons:
                try:
                    logger.info(f"Adding season: {season['year']}")
                    seasons_collection.add(season)
                    added_count += 1
                except Exception as e:
                    logger.error(f"Error adding season {season['year']}: {str(e)}")
            else:
                logger.info(f"Season {season['year']} already exists, skipping")
                skipped_count += 1
    
    logger.info(f"Seasons population complete! Added: {added_count}, Skipped: {skipped_count}")
    return added_count, skipped_count

def populate_races(db):
    """Add sample races to Firestore or in-memory database"""
    global in_memory_db
    added_count = 0
    skipped_count = 0
    
    # Combine all races
    all_races = races_2023 + races_2024
    
    if use_in_memory:
        # In-memory version
        existing_races = []
        for race in in_memory_db["races"]:
            if "name" in race and "date" in race:
                date_str = race["date"].strftime('%Y-%m-%d') if isinstance(race["date"], datetime.datetime) else str(race["date"])
                existing_races.append(f"{race['name']}_{date_str}")
        
        for race in all_races:
            race_key = f"{race['name']}_{race['date'].strftime('%Y-%m-%d')}"
            if race_key not in existing_races:
                logger.info(f"Adding race (in-memory): {race['name']} ({race['date'].strftime('%Y-%m-%d')})")
                race_copy = race.copy()
                race_copy['id'] = race_key  # Use race name and date as ID
                in_memory_db["races"].append(race_copy)
                added_count += 1
            else:
                logger.info(f"Race (in-memory) {race['name']} ({race['date'].strftime('%Y-%m-%d')}) already exists, skipping")
                skipped_count += 1
    else:
        # Firestore version
        races_collection = db.collection('races')
        
        # Check for existing races to avoid duplicates
        existing_races = []
        for doc in races_collection.stream():
            race_data = doc.to_dict()
            if "name" in race_data and "date" in race_data:
                # Convert Firestore Timestamp to datetime
                if isinstance(race_data['date'], firestore.firestore.Timestamp):
                    date_value = race_data['date'].datetime
                else:
                    date_value = race_data['date']
                
                existing_races.append(f"{race_data['name']}_{date_value.strftime('%Y-%m-%d')}")
        
        # Add races that don't already exist
        for race in all_races:
            race_key = f"{race['name']}_{race['date'].strftime('%Y-%m-%d')}"
            if race_key not in existing_races:
                try:
                    logger.info(f"Adding race: {race['name']} ({race['date'].strftime('%Y-%m-%d')})")
                    races_collection.add(race)
                    added_count += 1
                except Exception as e:
                    logger.error(f"Error adding race {race['name']}: {str(e)}")
            else:
                logger.info(f"Race {race['name']} ({race['date'].strftime('%Y-%m-%d')}) already exists, skipping")
                skipped_count += 1
    
    logger.info(f"Races population complete! Added: {added_count}, Skipped: {skipped_count}")
    return added_count, skipped_count

def export_in_memory_db():
    """Export the in-memory database to JSON files"""
    logger.info("Exporting in-memory database to JSON files...")
    
    # Create export directory if it doesn't exist
    export_dir = "db_export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Export each collection to a JSON file
    for collection, data in in_memory_db.items():
        file_path = os.path.join(export_dir, f"{collection}.json")
        
        # Convert datetime objects to strings for JSON serialization
        processed_data = []
        for item in data:
            item_copy = item.copy()
            for key, value in item_copy.items():
                if isinstance(value, datetime.datetime):
                    item_copy[key] = value.isoformat()
            processed_data.append(item_copy)
        
        # Write to file
        with open(file_path, 'w') as f:
            json.dump(processed_data, f, indent=2)
        
        logger.info(f"Exported {len(data)} {collection} to {file_path}")
    
    logger.info(f"Database export complete to directory: {export_dir}")

def populate_all_data():
    """Populate all collections in Firestore or in-memory database"""
    global use_in_memory
    
    # Initialize Firebase or use in-memory database
    db = initialize_firebase()
    
    if use_in_memory:
        logger.info("Using in-memory database for data storage")
    else:
        logger.info("Using Firebase Firestore for data storage")
    
    total_stats = {
        "teams": {"added": 0, "skipped": 0},
        "drivers": {"added": 0, "skipped": 0},
        "seasons": {"added": 0, "skipped": 0},
        "races": {"added": 0, "skipped": 0}
    }
    
    logger.info("Starting database population...")
    
    try:
        # First add teams (other collections may reference them)
        total_stats["teams"]["added"], total_stats["teams"]["skipped"] = populate_teams(db)
        time.sleep(1)  # Small delay to ensure teams are fully written
        
        # Then add drivers (which reference teams)
        total_stats["drivers"]["added"], total_stats["drivers"]["skipped"] = populate_drivers(db)
        time.sleep(1)
        
        # Add seasons
        total_stats["seasons"]["added"], total_stats["seasons"]["skipped"] = populate_seasons(db)
        time.sleep(1)
        
        # Add races (which reference drivers and seasons)
        total_stats["races"]["added"], total_stats["races"]["skipped"] = populate_races(db)
        
    except Exception as e:
        logger.error(f"Error during database population: {str(e)}")
        logger.warning("Switching to in-memory database mode")
        use_in_memory = True
        
        # Retry with in-memory database
        in_memory_db = {
            'teams': [],
            'drivers': [],
            'seasons': [],
            'races': []
        }
        
        # Populate in-memory database
        logger.info("Retrying with in-memory database...")
        total_stats["teams"]["added"], total_stats["teams"]["skipped"] = populate_teams(None)
        total_stats["drivers"]["added"], total_stats["drivers"]["skipped"] = populate_drivers(None)
        total_stats["seasons"]["added"], total_stats["seasons"]["skipped"] = populate_seasons(None)
        total_stats["races"]["added"], total_stats["races"]["skipped"] = populate_races(None)
        
        # Export in-memory database to JSON
        export_in_memory_db()
    
    logger.info("Database population complete!")
    
    # Print summary
    logger.info("\nSummary of database population:")
    for collection, stats in total_stats.items():
        logger.info(f"{collection.capitalize()}: {stats['added']} added, {stats['skipped']} skipped")
    
    return total_stats

if __name__ == "__main__":
    populate_all_data() 