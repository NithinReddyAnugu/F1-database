from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from main import db
from app.models.team import Team, TeamUpdate

router = APIRouter(prefix="/teams", tags=["Teams"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_teams(request: Request):
    """
    List all teams
    """
    teams_ref = db.collection("teams")
    teams = []
    for doc in teams_ref.stream():
        team_data = doc.to_dict()
        team_data["id"] = doc.id
        teams.append(team_data)
    
    return templates.TemplateResponse(
        "teams/list.html", 
        {"request": request, "teams": teams}
    )

@router.get("/add", response_class=HTMLResponse)
async def add_team_form(request: Request):
    """
    Render the form to add a new team
    """
    return templates.TemplateResponse(
        "teams/add.html", 
        {"request": request}
    )

@router.post("/add", response_class=HTMLResponse)
async def add_team(
    request: Request,
    name: str = Form(...),
    year_founded: int = Form(...),
    total_pole_positions: int = Form(...),
    total_race_wins: int = Form(...),
    total_constructor_titles: int = Form(...),
    finishing_position_previous_season: int = Form(...)
):
    """
    Add a new team
    """
    # Check if team with the same name already exists
    teams_ref = db.collection("teams")
    existing_teams = teams_ref.where("name", "==", name).stream()
    
    if any(True for _ in existing_teams):
        return templates.TemplateResponse(
            "teams/add.html",
            {
                "request": request,
                "error": "A team with this name already exists",
                "team": {
                    "name": name,
                    "year_founded": year_founded,
                    "total_pole_positions": total_pole_positions,
                    "total_race_wins": total_race_wins,
                    "total_constructor_titles": total_constructor_titles,
                    "finishing_position_previous_season": finishing_position_previous_season
                }
            }
        )
    
    # Validate team data
    try:
        team = Team(
            name=name,
            year_founded=year_founded,
            total_pole_positions=total_pole_positions,
            total_race_wins=total_race_wins,
            total_constructor_titles=total_constructor_titles,
            finishing_position_previous_season=finishing_position_previous_season
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "teams/add.html",
            {
                "request": request,
                "error": str(e),
                "team": {
                    "name": name,
                    "year_founded": year_founded,
                    "total_pole_positions": total_pole_positions,
                    "total_race_wins": total_race_wins,
                    "total_constructor_titles": total_constructor_titles,
                    "finishing_position_previous_season": finishing_position_previous_season
                }
            }
        )
    
    # Add team to Firestore
    teams_ref.add(team.dict())
    
    return RedirectResponse(url="/teams", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/{team_id}", response_class=HTMLResponse)
async def get_team(request: Request, team_id: str):
    """
    Get a team by ID
    """
    team_doc = db.collection("teams").document(team_id).get()
    
    if not team_doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = team_doc.to_dict()
    team_data["id"] = team_id
    
    # Get all drivers for this team
    drivers_ref = db.collection("drivers").where("team", "==", team_data["name"]).stream()
    drivers = []
    for doc in drivers_ref:
        driver_data = doc.to_dict()
        driver_data["id"] = doc.id
        drivers.append(driver_data)
    
    return templates.TemplateResponse(
        "teams/detail.html", 
        {"request": request, "team": team_data, "drivers": drivers}
    )

@router.get("/{team_id}/edit", response_class=HTMLResponse)
async def edit_team_form(request: Request, team_id: str):
    """
    Render the form to edit a team
    """
    team_doc = db.collection("teams").document(team_id).get()
    
    if not team_doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = team_doc.to_dict()
    team_data["id"] = team_id
    
    return templates.TemplateResponse(
        "teams/edit.html", 
        {"request": request, "team": team_data}
    )

@router.post("/{team_id}/edit", response_class=HTMLResponse)
async def edit_team(
    request: Request,
    team_id: str,
    year_founded: int = Form(...),
    total_pole_positions: int = Form(...),
    total_race_wins: int = Form(...),
    total_constructor_titles: int = Form(...),
    finishing_position_previous_season: int = Form(...)
):
    """
    Edit a team
    """
    team_doc = db.collection("teams").document(team_id).get()
    
    if not team_doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Validate team data
    try:
        team_update = TeamUpdate(
            year_founded=year_founded,
            total_pole_positions=total_pole_positions,
            total_race_wins=total_race_wins,
            total_constructor_titles=total_constructor_titles,
            finishing_position_previous_season=finishing_position_previous_season
        )
    except ValueError as e:
        team_data = team_doc.to_dict()
        team_data["id"] = team_id
        
        return templates.TemplateResponse(
            "teams/edit.html",
            {
                "request": request,
                "error": str(e),
                "team": team_data
            }
        )
    
    # Update team in Firestore
    db.collection("teams").document(team_id).update(team_update.dict(exclude_none=True))
    
    return RedirectResponse(url=f"/teams/{team_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/{team_id}/delete", response_class=HTMLResponse)
async def delete_team_confirmation(request: Request, team_id: str):
    """
    Render the confirmation page for deleting a team
    """
    team_doc = db.collection("teams").document(team_id).get()
    
    if not team_doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = team_doc.to_dict()
    team_data["id"] = team_id
    
    # Check if there are any drivers associated with this team
    drivers_ref = db.collection("drivers").where("team", "==", team_data["name"]).stream()
    has_drivers = any(True for _ in drivers_ref)
    
    return templates.TemplateResponse(
        "teams/delete.html", 
        {"request": request, "team": team_data, "has_drivers": has_drivers}
    )

@router.post("/{team_id}/delete", response_class=HTMLResponse)
async def delete_team(request: Request, team_id: str):
    """
    Delete a team
    """
    team_doc = db.collection("teams").document(team_id).get()
    
    if not team_doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = team_doc.to_dict()
    
    # Check if there are any drivers associated with this team
    drivers_ref = db.collection("drivers").where("team", "==", team_data["name"]).stream()
    if any(True for _ in drivers_ref):
        return templates.TemplateResponse(
            "teams/delete.html",
            {
                "request": request,
                "team": team_data,
                "has_drivers": True,
                "error": "Cannot delete team with associated drivers"
            }
        )
    
    # Delete team from Firestore
    db.collection("teams").document(team_id).delete()
    
    return RedirectResponse(url="/teams", status_code=status.HTTP_303_SEE_OTHER) 