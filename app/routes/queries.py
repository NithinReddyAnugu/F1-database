from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from main import db

router = APIRouter(prefix="/queries", tags=["Queries"])
templates = Jinja2Templates(directory="app/templates")

# Define the attributes that can be queried for drivers
DRIVER_ATTRIBUTES = {
    "age": "Age",
    "total_pole_positions": "Total Pole Positions",
    "total_race_wins": "Total Race Wins",
    "total_points_scored": "Total Points Scored",
    "total_world_titles": "Total World Titles",
    "total_fastest_laps": "Total Fastest Laps"
}

# Define the attributes that can be queried for teams
TEAM_ATTRIBUTES = {
    "year_founded": "Year Founded",
    "total_pole_positions": "Total Pole Positions",
    "total_race_wins": "Total Race Wins",
    "total_constructor_titles": "Total Constructor Titles",
    "finishing_position_previous_season": "Finishing Position in Previous Season"
}

# Define the comparison operators
COMPARISON_OPERATORS = {
    "lt": "Less Than",
    "eq": "Equal To",
    "gt": "Greater Than"
}

@router.get("/drivers", response_class=HTMLResponse)
async def query_drivers_form(request: Request):
    """
    Render the form to query drivers
    """
    return templates.TemplateResponse(
        "queries/drivers.html", 
        {
            "request": request, 
            "attributes": DRIVER_ATTRIBUTES,
            "operators": COMPARISON_OPERATORS
        }
    )

@router.post("/drivers", response_class=HTMLResponse)
async def query_drivers(
    request: Request,
    attribute: str = Form(...),
    operator: str = Form(...),
    value: str = Form(...)
):
    """
    Query drivers based on the selected attribute, operator, and value
    """
    # Validate the attribute
    if attribute not in DRIVER_ATTRIBUTES:
        raise HTTPException(status_code=400, detail="Invalid attribute")
    
    # Validate the operator
    if operator not in COMPARISON_OPERATORS:
        raise HTTPException(status_code=400, detail="Invalid operator")
    
    # Convert the value to the appropriate type
    try:
        if attribute in ["age", "total_pole_positions", "total_race_wins", "total_world_titles", "total_fastest_laps"]:
            value = int(value)
        elif attribute == "total_points_scored":
            value = float(value)
    except ValueError:
        return templates.TemplateResponse(
            "queries/drivers.html",
            {
                "request": request,
                "attributes": DRIVER_ATTRIBUTES,
                "operators": COMPARISON_OPERATORS,
                "error": f"Invalid value for {DRIVER_ATTRIBUTES[attribute]}"
            }
        )
    
    # Query Firestore
    drivers_ref = db.collection("drivers")
    
    if operator == "lt":
        query = drivers_ref.where(attribute, "<", value)
    elif operator == "eq":
        query = drivers_ref.where(attribute, "==", value)
    elif operator == "gt":
        query = drivers_ref.where(attribute, ">", value)
    
    # Execute the query
    drivers = []
    for doc in query.stream():
        driver_data = doc.to_dict()
        driver_data["id"] = doc.id
        drivers.append(driver_data)
    
    return templates.TemplateResponse(
        "queries/drivers_results.html",
        {
            "request": request,
            "drivers": drivers,
            "attribute": DRIVER_ATTRIBUTES[attribute],
            "operator": COMPARISON_OPERATORS[operator],
            "value": value
        }
    )

@router.get("/teams", response_class=HTMLResponse)
async def query_teams_form(request: Request):
    """
    Render the form to query teams
    """
    return templates.TemplateResponse(
        "queries/teams.html", 
        {
            "request": request, 
            "attributes": TEAM_ATTRIBUTES,
            "operators": COMPARISON_OPERATORS
        }
    )

@router.post("/teams", response_class=HTMLResponse)
async def query_teams(
    request: Request,
    attribute: str = Form(...),
    operator: str = Form(...),
    value: str = Form(...)
):
    """
    Query teams based on the selected attribute, operator, and value
    """
    # Validate the attribute
    if attribute not in TEAM_ATTRIBUTES:
        raise HTTPException(status_code=400, detail="Invalid attribute")
    
    # Validate the operator
    if operator not in COMPARISON_OPERATORS:
        raise HTTPException(status_code=400, detail="Invalid operator")
    
    # Convert the value to the appropriate type
    try:
        value = int(value)
    except ValueError:
        return templates.TemplateResponse(
            "queries/teams.html",
            {
                "request": request,
                "attributes": TEAM_ATTRIBUTES,
                "operators": COMPARISON_OPERATORS,
                "error": f"Invalid value for {TEAM_ATTRIBUTES[attribute]}"
            }
        )
    
    # Query Firestore
    teams_ref = db.collection("teams")
    
    if operator == "lt":
        query = teams_ref.where(attribute, "<", value)
    elif operator == "eq":
        query = teams_ref.where(attribute, "==", value)
    elif operator == "gt":
        query = teams_ref.where(attribute, ">", value)
    
    # Execute the query
    teams = []
    for doc in query.stream():
        team_data = doc.to_dict()
        team_data["id"] = doc.id
        teams.append(team_data)
    
    return templates.TemplateResponse(
        "queries/teams_results.html",
        {
            "request": request,
            "teams": teams,
            "attribute": TEAM_ATTRIBUTES[attribute],
            "operator": COMPARISON_OPERATORS[operator],
            "value": value
        }
    ) 