from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from main import db
from firebase_admin import firestore
import datetime

router = APIRouter(prefix="/seasons", tags=["Seasons"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_seasons(request: Request):
    """
    List all seasons
    """
    seasons_ref = db.collection("seasons").order_by("year", direction=firestore.Query.DESCENDING)
    seasons = []
    for doc in seasons_ref.stream():
        season_data = doc.to_dict()
        season_data["id"] = doc.id
        seasons.append(season_data)
    
    return templates.TemplateResponse(
        "seasons/list.html", 
        {"request": request, "seasons": seasons}
    )

@router.get("/add", response_class=HTMLResponse)
async def add_season_form(request: Request):
    """
    Render the form to add a new season
    """
    # Get all drivers and teams for the dropdowns
    drivers_ref = db.collection("drivers")
    drivers = []
    for doc in drivers_ref.stream():
        driver_data = doc.to_dict()
        driver_data["id"] = doc.id
        drivers.append(driver_data)
    
    teams_ref = db.collection("teams")
    teams = []
    for doc in teams_ref.stream():
        team_data = doc.to_dict()
        team_data["id"] = doc.id
        teams.append(team_data)
    
    return templates.TemplateResponse(
        "seasons/add.html", 
        {
            "request": request, 
            "drivers": drivers, 
            "teams": teams,
            "current_year": 2024  # Default to current year
        }
    )

@router.post("/add", response_class=HTMLResponse)
async def add_season(
    request: Request,
    year: int = Form(...),
    driver_champion_id: str = Form(...),
    team_champion_id: str = Form(...),
    total_races: int = Form(...),
    notable_event1: str = Form(...),
    notable_event2: Optional[str] = Form(None),
    notable_event3: Optional[str] = Form(None)
):
    """
    Add a new season
    """
    try:
        # Get driver and team champion information
        driver_doc = db.collection("drivers").document(driver_champion_id).get()
        team_doc = db.collection("teams").document(team_champion_id).get()
        
        if not driver_doc.exists or not team_doc.exists:
            raise HTTPException(status_code=404, detail="Driver or team not found")
        
        driver = driver_doc.to_dict()
        team = team_doc.to_dict()
        
        # Compile notable events
        notable_events = [notable_event1]
        if notable_event2:
            notable_events.append(notable_event2)
        if notable_event3:
            notable_events.append(notable_event3)
        
        # Create season document
        season_data = {
            "year": year,
            "driver_champion": driver["name"],
            "team_champion": team["name"],
            "total_races": total_races,
            "notable_events": notable_events
        }
        
        # Check if season already exists
        existing_seasons_query = db.collection("seasons").where("year", "==", year)
        existing_seasons = list(existing_seasons_query.stream())
        
        if existing_seasons:
            raise ValueError(f"Season for year {year} already exists")
        
        # Add to Firestore
        db.collection("seasons").add(season_data)
        
        return RedirectResponse(url="/seasons/", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as e:
        # Get all drivers and teams for the dropdowns (needed for form re-rendering)
        drivers_ref = db.collection("drivers")
        drivers = []
        for doc in drivers_ref.stream():
            driver_data = doc.to_dict()
            driver_data["id"] = doc.id
            drivers.append(driver_data)
        
        teams_ref = db.collection("teams")
        teams = []
        for doc in teams_ref.stream():
            team_data = doc.to_dict()
            team_data["id"] = doc.id
            teams.append(team_data)
        
        return templates.TemplateResponse(
            "seasons/add.html",
            {
                "request": request,
                "drivers": drivers,
                "teams": teams,
                "error": f"Error adding season: {str(e)}",
                "year": year,
                "total_races": total_races,
                "current_year": year  # Set current year to the input year
            }
        )

@router.get("/{season_id}", response_class=HTMLResponse)
async def view_season(request: Request, season_id: str):
    """
    View details of a specific season
    """
    season_doc = db.collection("seasons").document(season_id).get()
    
    if not season_doc.exists:
        raise HTTPException(status_code=404, detail="Season not found")
    
    season_data = season_doc.to_dict()
    season_data["id"] = season_id
    
    # Get races from this season
    year = season_data["year"]
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    # Convert to datetime objects for query
    start_datetime = firestore.firestore.SERVER_TIMESTAMP.from_datetime(
        datetime.datetime.strptime(start_date, "%Y-%m-%d")
    )
    end_datetime = firestore.firestore.SERVER_TIMESTAMP.from_datetime(
        datetime.datetime.strptime(end_date, "%Y-%m-%d")
    )
    
    races_query = db.collection("races").where("date", ">=", start_datetime).where("date", "<=", end_datetime).order_by("date")
    races = []
    for doc in races_query.stream():
        race_data = doc.to_dict()
        race_data["id"] = doc.id
        races.append(race_data)
    
    return templates.TemplateResponse(
        "seasons/view.html", 
        {
            "request": request, 
            "season": season_data,
            "races": races
        }
    )

@router.get("/delete/{season_id}", response_class=HTMLResponse)
async def delete_season_confirmation(request: Request, season_id: str):
    """
    Render confirmation page for season deletion
    """
    season_doc = db.collection("seasons").document(season_id).get()
    
    if not season_doc.exists:
        raise HTTPException(status_code=404, detail="Season not found")
    
    season_data = season_doc.to_dict()
    season_data["id"] = season_id
    
    return templates.TemplateResponse(
        "seasons/delete.html", 
        {"request": request, "season": season_data}
    )

@router.post("/delete/{season_id}", response_class=HTMLResponse)
async def delete_season(request: Request, season_id: str):
    """
    Delete a season
    """
    season_doc = db.collection("seasons").document(season_id).get()
    
    if not season_doc.exists:
        raise HTTPException(status_code=404, detail="Season not found")
    
    # Delete the season
    db.collection("seasons").document(season_id).delete()
    
    return RedirectResponse(url="/seasons/", status_code=status.HTTP_303_SEE_OTHER) 