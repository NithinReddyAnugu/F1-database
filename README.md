# F1-Database

A comprehensive Formula 1 statistics and data management application built with FastAPI and Firebase/Firestore, deployed on Google App Engine.

## Features

- **Team Management**: Add, edit, view, and delete Formula 1 teams with comprehensive statistics
- **Driver Management**: Track driver information, career statistics, and performance metrics
- **Advanced Queries**: Filter and search drivers and teams based on various criteria
- **Data Comparisons**: Compare statistics between drivers or teams
- **Authentication**: Secure access with Firebase Authentication
- **Responsive UI**: Modern, mobile-friendly interface

## Technologies Used

- **Backend**: FastAPI, Python 3.9+
- **Database**: Firebase/Firestore
- **Frontend**: HTML, CSS, JavaScript, Jinja2 Templates
- **Authentication**: Firebase Authentication
- **Deployment**: Google App Engine

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Firebase account with Firestore database
- Google Cloud account (for App Engine deployment)

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/NithinReddyAnugu/F1-Database.git
   cd F1-Database
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Firebase credentials:
   - Place your Firebase Admin SDK service account JSON file in the project root
   - Update the path in `main.py` if needed

4. Populate the database:
   ```
   python populate_db.py
   ```

5. Run the development server:
   ```
   python main.py
   ```

6. Access the application at http://localhost:8080

### Deployment to Google App Engine

1. Install the Google Cloud SDK
2. Configure the project:
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```
3. Deploy the application:
   ```
   gcloud app deploy
   ```

## Project Structure

- `/app`: Main application package
  - `/models`: Pydantic models for data validation
  - `/routes`: API endpoints and route handlers
  - `/static`: CSS, JavaScript, and other static assets
  - `/templates`: Jinja2 HTML templates
  - `/utils`: Utility functions and helpers
- `main.py`: Application entry point
- `populate_db.py`: Script to populate the database with sample data
- `app.yaml`: Google App Engine configuration
- `requirements.txt`: Python dependencies

## License

MIT License