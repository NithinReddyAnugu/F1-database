from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from main import db
from firebase_admin import firestore
import datetime

router = APIRouter(prefix="/races", tags=["Races"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_races(request: Request):
    """
    List all races
    """
    races_ref = db.collection("races").order_by("date", direction=firestore.Query.DESCENDING)
    races = []
    for doc in races_ref.stream():
        race_data = doc.to_dict()
        race_data["id"] = doc.id
        # Convert date to string for display
        if isinstance(race_data.get("date"), datetime.datetime):
            race_data["date_str"] = race_data["date"].strftime("%B %d, %Y")
        races.append(race_data)
    
    return templates.TemplateResponse(
        "races/list.html", 
        {"request": request, "races": races}
    )

@router.get("/add", response_class=HTMLResponse)
async def add_race_form(request: Request):
    """
    Render the form to add a new race
    """
    # Get all drivers for the dropdown
    drivers_ref = db.collection("drivers")
    drivers = []
    for doc in drivers_ref.stream():
        driver_data = doc.to_dict()
        driver_data["id"] = doc.id
        drivers.append(driver_data)
    
    return templates.TemplateResponse(
        "races/add.html", 
        {"request": request, "drivers": drivers}
    )

@router.post("/add", response_class=HTMLResponse)
async def add_race(
    request: Request,
    name: str = Form(...),
    circuit: str = Form(...),
    date: str = Form(...),
    winner_id: str = Form(...),
    second_id: str = Form(...),
    third_id: str = Form(...),
    fastest_lap_id: str = Form(...)
):
    """
    Add a new race
    """
    try:
        # Parse date
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        
        # Get driver information
        winner_doc = db.collection("drivers").document(winner_id).get()
        second_doc = db.collection("drivers").document(second_id).get()
        third_doc = db.collection("drivers").document(third_id).get()
        fastest_lap_doc = db.collection("drivers").document(fastest_lap_id).get()
        
        if not all([winner_doc.exists, second_doc.exists, third_doc.exists, fastest_lap_doc.exists]):
            raise HTTPException(status_code=404, detail="One or more drivers not found")
        
        winner = winner_doc.to_dict()
        second = second_doc.to_dict()
        third = third_doc.to_dict()
        fastest_lap = fastest_lap_doc.to_dict()
        
        # Create race results
        results = [
            {
                "driver": winner["name"],
                "position": 1,
                "points": 25 if winner["name"] == fastest_lap["name"] else 25,
                "fastest_lap": winner["name"] == fastest_lap["name"]
            },
            {
                "driver": second["name"],
                "position": 2,
                "points": 18 if second["name"] == fastest_lap["name"] else 18,
                "fastest_lap": second["name"] == fastest_lap["name"]
            },
            {
                "driver": third["name"],
                "position": 3,
                "points": 15 if third["name"] == fastest_lap["name"] else 15,
                "fastest_lap": third["name"] == fastest_lap["name"]
            }
        ]
        
        # If fastest lap driver is not in top 3, add them to results
        if fastest_lap["name"] not in [winner["name"], second["name"], third["name"]]:
            # We'll assume they finished 4th for simplicity
            results.append({
                "driver": fastest_lap["name"],
                "position": 4,
                "points": 12 + 1,  # 12 points for 4th + 1 for fastest lap
                "fastest_lap": True
            })
        
        # Create race document
        race_data = {
            "name": name,
            "circuit": circuit,
            "date": date_obj,
            "results": results
        }
        
        # Add to Firestore
        db.collection("races").add(race_data)
        
        return RedirectResponse(url="/races/", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as e:
        # Get all drivers for the dropdown (needed for form re-rendering)
        drivers_ref = db.collection("drivers")
        drivers = []
        for doc in drivers_ref.stream():
            driver_data = doc.to_dict()
            driver_data["id"] = doc.id
            drivers.append(driver_data)
        
        return templates.TemplateResponse(
            "races/add.html",
            {
                "request": request,
                "drivers": drivers,
                "error": f"Error adding race: {str(e)}",
                "name": name,
                "circuit": circuit,
                "date": date
            }
        )

@router.get("/{race_id}", response_class=HTMLResponse)
async def view_race(request: Request, race_id: str):
    """
    View details of a specific race
    """
    race_doc = db.collection("races").document(race_id).get()
    
    if not race_doc.exists:
        raise HTTPException(status_code=404, detail="Race not found")
    
    race_data = race_doc.to_dict()
    race_data["id"] = race_id
    
    # Convert date to string for display
    if isinstance(race_data.get("date"), datetime.datetime):
        race_data["date_str"] = race_data["date"].strftime("%B %d, %Y")
    
    return templates.TemplateResponse(
        "races/view.html", 
        {"request": request, "race": race_data}
    )

@router.get("/delete/{race_id}", response_class=HTMLResponse)
async def delete_race_confirmation(request: Request, race_id: str):
    """
    Render confirmation page for race deletion
    """
    race_doc = db.collection("races").document(race_id).get()
    
    if not race_doc.exists:
        raise HTTPException(status_code=404, detail="Race not found")
    
    race_data = race_doc.to_dict()
    race_data["id"] = race_id
    
    return templates.TemplateResponse(
        "races/delete.html", 
        {"request": request, "race": race_data}
    )

@router.post("/delete/{race_id}", response_class=HTMLResponse)
async def delete_race(request: Request, race_id: str):
    """
    Delete a race
    """
    race_doc = db.collection("races").document(race_id).get()
    
    if not race_doc.exists:
        raise HTTPException(status_code=404, detail="Race not found")
    
    # Delete the race
    db.collection("races").document(race_id).delete()
    
    return RedirectResponse(url="/races/", status_code=status.HTTP_303_SEE_OTHER) 