from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from main import db

router = APIRouter(prefix="/comparisons", tags=["Comparisons"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/drivers", response_class=HTMLResponse)
async def compare_drivers_form(request: Request):
    """
    Render the form to compare two drivers
    """
    # Get all drivers for the dropdowns
    drivers_ref = db.collection("drivers")
    drivers = []
    for doc in drivers_ref.stream():
        driver_data = doc.to_dict()
        driver_data["id"] = doc.id
        drivers.append(driver_data)
    
    return templates.TemplateResponse(
        "comparisons/drivers.html", 
        {"request": request, "drivers": drivers}
    )

@router.post("/drivers", response_class=HTMLResponse)
async def compare_drivers(
    request: Request,
    driver1_id: str = Form(...),
    driver2_id: str = Form(...)
):
    """
    Compare two drivers
    """
    # Validate that two different drivers were selected
    if driver1_id == driver2_id:
        # Get all drivers for the dropdowns
        drivers_ref = db.collection("drivers")
        drivers = []
        for doc in drivers_ref.stream():
            driver_data = doc.to_dict()
            driver_data["id"] = doc.id
            drivers.append(driver_data)
        
        return templates.TemplateResponse(
            "comparisons/drivers.html",
            {
                "request": request,
                "drivers": drivers,
                "error": "Please select two different drivers"
            }
        )
    
    # Get the drivers from Firestore
    driver1_doc = db.collection("drivers").document(driver1_id).get()
    driver2_doc = db.collection("drivers").document(driver2_id).get()
    
    if not driver1_doc.exists or not driver2_doc.exists:
        raise HTTPException(status_code=404, detail="One or both drivers not found")
    
    driver1_data = driver1_doc.to_dict()
    driver1_data["id"] = driver1_id
    
    driver2_data = driver2_doc.to_dict()
    driver2_data["id"] = driver2_id
    
    # Determine which driver has better stats for each attribute
    comparison = {
        "age": "driver1" if driver1_data["age"] < driver2_data["age"] else "driver2" if driver2_data["age"] < driver1_data["age"] else "equal",
        "total_pole_positions": "driver1" if driver1_data["total_pole_positions"] > driver2_data["total_pole_positions"] else "driver2" if driver2_data["total_pole_positions"] > driver1_data["total_pole_positions"] else "equal",
        "total_race_wins": "driver1" if driver1_data["total_race_wins"] > driver2_data["total_race_wins"] else "driver2" if driver2_data["total_race_wins"] > driver1_data["total_race_wins"] else "equal",
        "total_points_scored": "driver1" if driver1_data["total_points_scored"] > driver2_data["total_points_scored"] else "driver2" if driver2_data["total_points_scored"] > driver1_data["total_points_scored"] else "equal",
        "total_world_titles": "driver1" if driver1_data["total_world_titles"] > driver2_data["total_world_titles"] else "driver2" if driver2_data["total_world_titles"] > driver1_data["total_world_titles"] else "equal",
        "total_fastest_laps": "driver1" if driver1_data["total_fastest_laps"] > driver2_data["total_fastest_laps"] else "driver2" if driver2_data["total_fastest_laps"] > driver1_data["total_fastest_laps"] else "equal"
    }
    
    return templates.TemplateResponse(
        "comparisons/drivers_results.html",
        {
            "request": request,
            "driver1": driver1_data,
            "driver2": driver2_data,
            "comparison": comparison
        }
    )

@router.get("/teams", response_class=HTMLResponse)
async def compare_teams_form(request: Request):
    """
    Render the form to compare two teams
    """
    # Get all teams for the dropdowns
    teams_ref = db.collection("teams")
    teams = []
    for doc in teams_ref.stream():
        team_data = doc.to_dict()
        team_data["id"] = doc.id
        teams.append(team_data)
    
    return templates.TemplateResponse(
        "comparisons/teams.html", 
        {"request": request, "teams": teams}
    )

@router.post("/teams", response_class=HTMLResponse)
async def compare_teams(
    request: Request,
    team1_id: str = Form(...),
    team2_id: str = Form(...)
):
    """
    Compare two teams
    """
    # Validate that two different teams were selected
    if team1_id == team2_id:
        # Get all teams for the dropdowns
        teams_ref = db.collection("teams")
        teams = []
        for doc in teams_ref.stream():
            team_data = doc.to_dict()
            team_data["id"] = doc.id
            teams.append(team_data)
        
        return templates.TemplateResponse(
            "comparisons/teams.html",
            {
                "request": request,
                "teams": teams,
                "error": "Please select two different teams"
            }
        )
    
    # Get the teams from Firestore
    team1_doc = db.collection("teams").document(team1_id).get()
    team2_doc = db.collection("teams").document(team2_id).get()
    
    if not team1_doc.exists or not team2_doc.exists:
        raise HTTPException(status_code=404, detail="One or both teams not found")
    
    team1_data = team1_doc.to_dict()
    team1_data["id"] = team1_id
    
    team2_data = team2_doc.to_dict()
    team2_data["id"] = team2_id
    
    # Determine which team has better stats for each attribute
    comparison = {
        "year_founded": "team1" if team1_data["year_founded"] < team2_data["year_founded"] else "team2" if team2_data["year_founded"] < team1_data["year_founded"] else "equal",
        "total_pole_positions": "team1" if team1_data["total_pole_positions"] > team2_data["total_pole_positions"] else "team2" if team2_data["total_pole_positions"] > team1_data["total_pole_positions"] else "equal",
        "total_race_wins": "team1" if team1_data["total_race_wins"] > team2_data["total_race_wins"] else "team2" if team2_data["total_race_wins"] > team1_data["total_race_wins"] else "equal",
        "total_constructor_titles": "team1" if team1_data["total_constructor_titles"] > team2_data["total_constructor_titles"] else "team2" if team2_data["total_constructor_titles"] > team1_data["total_constructor_titles"] else "equal",
        "finishing_position_previous_season": "team1" if team1_data["finishing_position_previous_season"] < team2_data["finishing_position_previous_season"] else "team2" if team2_data["finishing_position_previous_season"] < team1_data["finishing_position_previous_season"] else "equal"
    }
    
    return templates.TemplateResponse(
        "comparisons/teams_results.html",
        {
            "request": request,
            "team1": team1_data,
            "team2": team2_data,
            "comparison": comparison
        }
    ) 