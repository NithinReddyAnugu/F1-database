# F1-Database 🏎️

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/2560px-F1.svg.png" alt="F1 Logo" width="300"/>
  
  <p>A comprehensive Formula 1 database application that allows users to explore information about F1 drivers, teams, races, and seasons.</p>
  
  <p>
    <a href="https://createproject-451614.uc.r.appspot.com" target="_blank">🌐 Live Demo</a> •
    <a href="#features">✨ Features</a> •
    <a href="#technologies">🔧 Technologies</a> •
    <a href="#installation">🚀 Installation</a> •
    <a href="#deployment">☁️ Deployment</a>
  </p>
</div>

## 📋 Overview

The F1-Database is a full-featured web application that provides detailed information about Formula 1 teams, drivers, races, and seasons. Users can browse, query, and compare F1 data, with authenticated users able to perform administrative operations.

## ✨ Features <a name="features"></a>

- View detailed information about Formula 1 drivers and teams
- Query drivers and teams based on various attributes (age, wins, championships, etc.)
- Compare two drivers or teams side by side with visual stat comparison
- Firebase authentication for admin operations (add, edit, delete)
- Firestore database for reliable and scalable data storage
- Responsive design for desktop and mobile viewing

## 🔧 Technologies <a name="technologies"></a>

<div align="center">
  <table>
    <tr>
      <td align="center" width="96">
        <img src="https://cdn.worldvectorlogo.com/logos/fastapi-1.svg" width="48" height="48" alt="FastAPI" />
        <br>FastAPI
      </td>
      <td align="center" width="96">
        <img src="https://www.vectorlogo.zone/logos/firebase/firebase-icon.svg" width="48" height="48" alt="Firebase" />
        <br>Firebase
      </td>
      <td align="center" width="96">
        <img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" width="48" height="48" alt="Google Cloud" />
        <br>GCP
      </td>
      <td align="center" width="96">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="48" height="48" alt="Python" />
        <br>Python
      </td>
      <td align="center" width="96">
        <img src="https://cdn.worldvectorlogo.com/logos/bootstrap-5-1.svg" width="48" height="48" alt="Bootstrap" />
        <br>Bootstrap
      </td>
    </tr>
  </table>
</div>

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python, FastAPI
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **Deployment**: Google App Engine
- **CI/CD**: GitHub Actions

## 🚀 Installation and Setup <a name="installation"></a>

### Prerequisites

- Python 3.9 or higher
- Firebase account and project
- Google Cloud account (for deployment)

### Local Development Setup

1. Clone the repository:
```
git clone https://github.com/NithinReddyAnugu/F1-database.git
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

4. Make sure you have the Firebase service account key file (JSON) in the project root:
```
f1formula-f6f18-firebase-adminsdk-fbsvc-74edc3c8b3.json
```

5. Run the application locally:
```
python -m uvicorn main:app --reload
```


## 💾 Database Population

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

## 📁 Project Structure

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
└── README.md            # Project documentation
```

## 🔌 API Endpoints

The application provides various API endpoints for accessing and manipulating the data:

| Endpoint | Description | Auth Required |
|----------|-------------|---------------|
| `/drivers` | List all drivers | No |
| `/drivers/{driver_name}` | Get driver details | No |
| `/drivers/{driver_name}` | Update/delete driver | Yes |
| `/teams` | List all teams | No |
| `/teams/{team_name}` | Get team details | No |
| `/teams/{team_name}` | Update/delete team | Yes |
| `/queries/drivers` | Query drivers based on attributes | No |
| `/queries/teams` | Query teams based on attributes | No |
| `/comparisons/drivers` | Compare two drivers | No |
| `/comparisons/teams` | Compare two teams | No |
| `/races` | List races and results | No |

## 🔐 Authentication

The application uses Firebase Authentication for user management. To add, edit, or delete information, users must log in with their Google account or email/password.

## ☁️ Deployment <a name="deployment"></a>

### Google App Engine Deployment

This application is deployed on [Google App Engine](https://cloud.google.com/appengine) at:
- https://createproject-451614.uc.r.appspot.com

To deploy your own instance:

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install):
   - Windows: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
   - Mac/Linux: `curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-VERSION-OS.tar.gz`

2. Authenticate with Google Cloud:
```
gcloud auth login
```

3. Set the project ID:
```
gcloud config set project YOUR_PROJECT_ID
```

4. Deploy the application:
```
gcloud app deploy
```

5. Visit the deployed application:
```
gcloud app browse
```

### Key Deployment Files

- **app.yaml**: Contains the Google App Engine configuration
  ```yaml
  runtime: python39
  instance_class: F2
  entrypoint: gunicorn -b :$PORT -k uvicorn.workers.UvicornWorker main:app --timeout 300
  ```

- **requirements.txt**: Lists all Python dependencies for deployment
  ```
  firebase-admin==6.2.0
  fastapi==0.103.1
  uvicorn==0.23.2
  gunicorn==21.2.0
  # ... other dependencies
  ```

## 📃 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Nithin Reddy Anugu

---

<div align="center">
  <p>Deployed on <a href="https://cloud.google.com/appengine" target="_blank">Google App Engine</a> | Powered by <a href="https://firebase.google.com/" target="_blank">Firebase</a></p>
  <p>
    <a href="https://fastapi.tiangolo.com/"><img src="https://cdn.worldvectorlogo.com/logos/fastapi-1.svg" height="30"></a> &nbsp;
    <a href="https://firebase.google.com/"><img src="https://www.vectorlogo.zone/logos/firebase/firebase-icon.svg" height="30"></a> &nbsp;
    <a href="https://cloud.google.com/"><img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" height="30"></a>
  </p>
</div>
