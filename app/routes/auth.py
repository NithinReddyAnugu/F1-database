from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request as StarletteRequest

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Render the login page
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/check-auth")
async def check_auth(request: Request):
    """
    Check if a user is authenticated
    """
    # This endpoint will be called by client-side JavaScript to check authentication status
    # The actual authentication is handled by Firebase on the client side
    return {"message": "Authentication check endpoint"} 