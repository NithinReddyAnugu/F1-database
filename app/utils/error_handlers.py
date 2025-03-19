from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import firebase_admin.exceptions
from google.cloud.firestore import NotFound

# Setup templates reference
templates = Jinja2Templates(directory="app/templates")

class FirebaseError(HTTPException):
    """Custom exception for Firebase related errors"""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

async def firebase_exception_handler(request: Request, exc: firebase_admin.exceptions.FirebaseError):
    """Handle Firebase exceptions by redirecting to an error page"""
    if isinstance(exc, NotFound):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "The requested resource was not found"
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = f"Database error: {str(exc)}"
    
    # If the request expects HTML, return an HTML error page
    if request.headers.get("accept", "").find("text/html") != -1:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": status_code, "detail": detail},
            status_code=status_code
        )
    
    # Otherwise return a JSON response
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail}
    )

async def validation_exception_handler(request: Request, exc: HTTPException):
    """Handle validation exceptions from Pydantic models"""
    status_code = exc.status_code
    detail = str(exc.detail)
    
    # If the request expects HTML, return an HTML error page
    if request.headers.get("accept", "").find("text/html") != -1:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": status_code, "detail": detail},
            status_code=status_code
        )
    
    # Otherwise return a JSON response
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail}
    )

def setup_error_handlers(app):
    """Register all error handlers with the FastAPI application"""
    app.add_exception_handler(firebase_admin.exceptions.FirebaseError, firebase_exception_handler)
    app.add_exception_handler(HTTPException, validation_exception_handler) 