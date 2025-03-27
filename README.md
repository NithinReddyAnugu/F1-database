# F1-Database

A comprehensive Formula 1 database application that allows users to explore information about F1 drivers, teams, races, and seasons.

## Features

- View detailed information about Formula 1 drivers and teams
- Query drivers and teams based on various attributes
- Compare two drivers or teams side by side
- Firebase authentication for admin operations
- Firestore database for data storage

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python, FastAPI
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **Deployment**: Google App Engine

## Installation and Setup

### Prerequisites

- Python 3.9 or higher
- Firebase account and project
- Google Cloud account (for deployment)

### Local Development Setup

1. Clone the repository:
```
git clone https://github.com/your-username/F1-Database.git
cd F1-Database
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Add your Firebase service account key file (JSON) to the project root.

5. Run the application:
```
python -m uvicorn main:app --reload
```

6. Visit `http://localhost:8000` in your browser.

## Database Population

The application uses Firebase Firestore as the database. You can populate the database with sample data using the provided scripts:

### Comprehensive Data Population

To populate all collections at once (teams, drivers, seasons, races):

```
python populate_all_data.py
```

This script will:
- Add teams data first (since other collections reference teams)
- Add drivers data (which reference teams)
- Add seasons data
- Add race results data (which reference drivers and seasons)

The script is designed to be idempotent - it will not add duplicate entries if run multiple times.

### Individual Collection Population

You can also populate specific collections individually:

- For teams and drivers: `python populate_db.py`
- For races: `python populate_races.py`
- For seasons: `python populate_seasons.py`

## Project Structure

```
F1-Database/
├── app/
│   ├── models/          # Pydantic models
│   ├── routes/          # API routes
│   ├── static/          # Static files (CSS, JS)
│   ├── templates/       # HTML templates
│   └── utils/           # Utility functions
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── app.yaml             # Google App Engine configuration
├── populate_all_data.py # Script to populate all database collections
├── populate_db.py       # Script to populate teams and drivers
├── populate_races.py    # Script to populate races
└── populate_seasons.py  # Script to populate seasons
```

## API Endpoints

The application provides various API endpoints for accessing and manipulating the data:

- `/drivers` - List all drivers
- `/drivers/{driver_name}` - Get, update, or delete a specific driver
- `/teams` - List all teams
- `/teams/{team_name}` - Get, update, or delete a specific team
- `/queries/drivers` - Query drivers based on attributes
- `/queries/teams` - Query teams based on attributes
- `/comparisons/drivers` - Compare two drivers
- `/comparisons/teams` - Compare two teams
- `/races` - List races and results

## Authentication

The application uses Firebase Authentication for user management. To add, edit, or delete information, users must log in with their Google account or email/password.

## Deployment

### Google App Engine

1. Install and set up the Google Cloud SDK.
2. Authenticate with Google Cloud:
```
gcloud auth login
```

3. Set the project ID:
```
gcloud config set project [YOUR_PROJECT_ID]
```

4. Deploy the application:
```
gcloud app deploy
```

5. Visit the deployed application:
```
gcloud app browse
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name - Initial work