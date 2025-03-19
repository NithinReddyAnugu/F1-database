from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from main import db
from app.models.driver import Driver, DriverUpdate

router = APIRouter(prefix="/drivers", tags=["Drivers"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_drivers(request: Request):
    """
    List all drivers
    """
    drivers_ref = db.collection("drivers")
    drivers = []
    for doc in drivers_ref.stream():
        driver_data = doc.to_dict()
        driver_data["id"] = doc.id
        drivers.append(driver_data)
    
    return templates.TemplateResponse(
        "drivers/list.html", 
        {"request": request, "drivers": drivers}
    )

@router.get("/add", response_class=HTMLResponse)
async def add_driver_form(request: Request):
    """
    Render the form to add a new driver
    """
    # Get all teams for the dropdown
    teams_ref = db.collection("teams")
    teams = []
    for doc in teams_ref.stream():
        teams.append({"id": doc.id, "name": doc.to_dict()["name"]})
    
    return templates.TemplateResponse(
        "drivers/add.html", 
        {"request": request, "teams": teams}
    )

@router.post("/add", response_class=HTMLResponse)
async def add_driver(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    total_pole_positions: int = Form(...),
    total_race_wins: int = Form(...),
    total_points_scored: float = Form(...),
    total_world_titles: int = Form(...),
    total_fastest_laps: int = Form(...),
    team: str = Form(...)
):
    """
    Add a new driver
    """
    # Check if driver with the same name already exists
    drivers_ref = db.collection("drivers")
    existing_drivers = drivers_ref.where("name", "==", name).stream()
    
    if any(True for _ in existing_drivers):
        return templates.TemplateResponse(
            "drivers/add.html",
            {
                "request": request,
                "error": "A driver with this name already exists",
                "driver": {
                    "name": name,
                    "age": age,
                    "total_pole_positions": total_pole_positions,
                    "total_race_wins": total_race_wins,
                    "total_points_scored": total_points_scored,
                    "total_world_titles": total_world_titles,
                    "total_fastest_laps": total_fastest_laps,
                    "team": team
                }
            }
        )
    
    # Validate driver data
    try:
        driver = Driver(
            name=name,
            age=age,
            total_pole_positions=total_pole_positions,
            total_race_wins=total_race_wins,
            total_points_scored=total_points_scored,
            total_world_titles=total_world_titles,
            total_fastest_laps=total_fastest_laps,
            team=team
        )
    except ValueError as e:
        # Get all teams for the dropdown
        teams_ref = db.collection("teams")
        teams = []
        for doc in teams_ref.stream():
            teams.append({"id": doc.id, "name": doc.to_dict()["name"]})
            
        return templates.TemplateResponse(
            "drivers/add.html",
            {
                "request": request,
                "error": str(e),
                "driver": {
                    "name": name,
                    "age": age,
                    "total_pole_positions": total_pole_positions,
                    "total_race_wins": total_race_wins,
                    "total_points_scored": total_points_scored,
                    "total_world_titles": total_world_titles,
                    "total_fastest_laps": total_fastest_laps,
                    "team": team
                },
                "teams": teams
            }
        )
    
    # Add driver to Firestore
    drivers_ref.add(driver.dict())
    
    return RedirectResponse(url="/drivers", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/{driver_id}", response_class=HTMLResponse)
async def get_driver(request: Request, driver_id: str):
    """
    Get a driver by ID
    """
    driver_doc = db.collection("drivers").document(driver_id).get()
    
    if not driver_doc.exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver_data = driver_doc.to_dict()
    driver_data["id"] = driver_id
    
    return templates.TemplateResponse(
        "drivers/detail.html", 
        {"request": request, "driver": driver_data}
    )

@router.get("/{driver_id}/edit", response_class=HTMLResponse)
async def edit_driver_form(request: Request, driver_id: str):
    """
    Render the form to edit a driver
    """
    driver_doc = db.collection("drivers").document(driver_id).get()
    
    if not driver_doc.exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver_data = driver_doc.to_dict()
    driver_data["id"] = driver_id
    
    # Get all teams for the dropdown
    teams_ref = db.collection("teams")
    teams = []
    for doc in teams_ref.stream():
        teams.append({"id": doc.id, "name": doc.to_dict()["name"]})
    
    return templates.TemplateResponse(
        "drivers/edit.html", 
        {"request": request, "driver": driver_data, "teams": teams}
    )

@router.post("/{driver_id}/edit", response_class=HTMLResponse)
async def edit_driver(
    request: Request,
    driver_id: str,
    age: int = Form(...),
    total_pole_positions: int = Form(...),
    total_race_wins: int = Form(...),
    total_points_scored: float = Form(...),
    total_world_titles: int = Form(...),
    total_fastest_laps: int = Form(...),
    team: str = Form(...)
):
    """
    Edit a driver
    """
    driver_doc = db.collection("drivers").document(driver_id).get()
    
    if not driver_doc.exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    # Validate driver data
    try:
        driver_update = DriverUpdate(
            age=age,
            total_pole_positions=total_pole_positions,
            total_race_wins=total_race_wins,
            total_points_scored=total_points_scored,
            total_world_titles=total_world_titles,
            total_fastest_laps=total_fastest_laps,
            team=team
        )
    except ValueError as e:
        driver_data = driver_doc.to_dict()
        driver_data["id"] = driver_id
        
        # Get all teams for the dropdown
        teams_ref = db.collection("teams")
        teams = []
        for doc in teams_ref.stream():
            teams.append({"id": doc.id, "name": doc.to_dict()["name"]})
            
        return templates.TemplateResponse(
            "drivers/edit.html",
            {
                "request": request,
                "error": str(e),
                "driver": driver_data,
                "teams": teams
            }
        )
    
    # Update driver in Firestore
    db.collection("drivers").document(driver_id).update(driver_update.dict(exclude_none=True))
    
    return RedirectResponse(url=f"/drivers/{driver_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/{driver_id}/delete", response_class=HTMLResponse)
async def delete_driver_confirmation(request: Request, driver_id: str):
    """
    Render the confirmation page for deleting a driver
    """
    driver_doc = db.collection("drivers").document(driver_id).get()
    
    if not driver_doc.exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver_data = driver_doc.to_dict()
    driver_data["id"] = driver_id
    
    return templates.TemplateResponse(
        "drivers/delete.html", 
        {"request": request, "driver": driver_data}
    )

@router.post("/{driver_id}/delete", response_class=HTMLResponse)
async def delete_driver(request: Request, driver_id: str):
    """
    Delete a driver
    """
    driver_doc = db.collection("drivers").document(driver_id).get()
    
    if not driver_doc.exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    # Delete driver from Firestore
    db.collection("drivers").document(driver_id).delete()
    
    return RedirectResponse(url="/drivers", status_code=status.HTTP_303_SEE_OTHER) 