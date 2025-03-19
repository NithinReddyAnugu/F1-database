"""
Utility functions for the F1-Database application.
"""

from app.utils.error_handlers import setup_error_handlers, FirebaseError
from app.utils.validators import (
    validate_driver_exists,
    validate_team_exists,
    validate_team_name_exists,
    validate_unique_driver_name,
    validate_unique_team_name
) 