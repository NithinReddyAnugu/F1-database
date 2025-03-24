from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class RaceResult(BaseModel):
    """
    Model representing a single driver's result in a race
    """
    driver: str
    position: int = Field(..., gt=0)
    points: float = Field(..., ge=0)
    fastest_lap: bool = False
    dnf: bool = False  # Did Not Finish
    
    @validator('driver')
    def driver_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Driver name cannot be empty')
        return v.strip()

class Race(BaseModel):
    """
    Model representing a Formula 1 race
    """
    name: str
    circuit: str
    date: datetime
    season: int = Field(..., ge=1950)
    results: List[RaceResult] = []
    
    @validator('name', 'circuit')
    def field_must_not_be_empty(cls, v, field):
        if not v.strip():
            raise ValueError(f'{field.name} cannot be empty')
        return v.strip()
    
    @validator('date')
    def date_must_be_valid(cls, v):
        if v > datetime.now():
            raise ValueError('Race date cannot be in the future')
        return v
    
    @validator('season')
    def season_must_be_valid(cls, v):
        current_year = datetime.now().year
        if v < 1950 or v > current_year:
            raise ValueError(f'Season must be between 1950 and {current_year}')
        return v

class RaceUpdate(BaseModel):
    """
    Model for updating race information
    """
    name: Optional[str] = None
    circuit: Optional[str] = None
    date: Optional[datetime] = None
    season: Optional[int] = Field(None, ge=1950)
    results: Optional[List[RaceResult]] = None
    
    @validator('name', 'circuit')
    def field_must_not_be_empty(cls, v, field):
        if v is not None and not v.strip():
            raise ValueError(f'{field.name} cannot be empty')
        return v.strip() if v else v
    
    @validator('date')
    def date_must_be_valid(cls, v):
        if v is not None and v > datetime.now():
            raise ValueError('Race date cannot be in the future')
        return v
    
    @validator('season')
    def season_must_be_valid(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1950 or v > current_year:
                raise ValueError(f'Season must be between 1950 and {current_year}')
        return v 