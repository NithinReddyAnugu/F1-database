from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request as StarletteRequest
import firebase_admin
from firebase_admin import auth
import json

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

@router.get("/auth-callback")
async def auth_callback():
    """
    Handle auth callback from Firebase
    """
    return RedirectResponse(url="/")

@router.post("/token-verify")
async def verify_token(request: Request):
    """
    Verify Firebase token
    """
    try:
        data = await request.json()
        token = data.get("token")
        
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "No authentication token provided"}
            )
        
        try:
            # Verify the Firebase token
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            
            # In a full implementation, you might want to check if the user exists in your database
            # and handle user sessions or create JWT tokens for your own backend
            
            return {
                "message": "Token verified successfully",
                "user": {
                    "uid": uid,
                    "email": email
                }
            }
        except Exception as e:
            # Handle verification errors
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": f"Invalid authentication token: {str(e)}"}
            )
    except Exception as e:
        # Handle general errors
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Error processing request: {str(e)}"}
        ) 