from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import firebase_admin
from firebase_admin import credentials, firestore
import os
import uvicorn

# Initialize Firebase Admin SDK
try:
    # Check for environment variable first
    firebase_config_file = os.environ.get('FIREBASE_CONFIG_FILE')
    
    # Try multiple possible credential file paths
    potential_credential_files = []
    
    # First priority: environment variable if set
    if firebase_config_file and os.path.exists(firebase_config_file):
        potential_credential_files.append(firebase_config_file)
    
    # Add other possible files
    potential_credential_files.extend([
        "f1formula-f6f18-firebase-adminsdk-fbsvc-74edc3c8b3.json",  # Correct file
        "firebase-credentials.json"  # Generic name
    ])
    
    # Find the first valid credential file
    cred_path = None
    for file_path in potential_credential_files:
        if os.path.exists(file_path):
            print(f"Found credential file: {file_path}")
            cred_path = file_path
            break
    
    if not cred_path:
        raise FileNotFoundError("No valid Firebase credential file found. Please make sure the credential file exists.")
    
    # Initialize Firebase
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully")
except ValueError:
    # App already initialized
    print("Firebase app already initialized")
except Exception as e:
    print(f"Error initializing Firebase: {str(e)}")
    raise

# Initialize Firestore client
db = firestore.client()

# Create FastAPI app
app = FastAPI(title="Formula 1 Database")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Import routes
from app.routes import auth, drivers, teams, queries, comparisons, races

# Include routers
app.include_router(auth.router)
app.include_router(drivers.router)
app.include_router(teams.router)
app.include_router(queries.router)
app.include_router(comparisons.router)
app.include_router(races.router)

# Setup error handlers
from app.utils.error_handlers import setup_error_handlers
setup_error_handlers(app)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint that renders the home page
    """
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) 