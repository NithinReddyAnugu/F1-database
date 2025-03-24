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
    cred = credentials.Certificate("f1formula-f6f18-firebase-adminsdk-fbsvc-89d270ff8f.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized
    pass

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