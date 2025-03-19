from pydantic import BaseModel, Field, validator
from typing import Optional

class Driver(BaseModel):
    """
    Model representing a Formula 1 driver
    """
    name: str
    age: int = Field(..., gt=0)
    total_pole_positions: int = Field(..., ge=0)
    total_race_wins: int = Field(..., ge=0)
    total_points_scored: float = Field(..., ge=0)
    total_world_titles: int = Field(..., ge=0)
    total_fastest_laps: int = Field(..., ge=0)
    team: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @validator('team')
    def team_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Team cannot be empty')
        return v.strip()

class DriverUpdate(BaseModel):
    """
    Model for updating a driver's information
    """
    age: Optional[int] = Field(None, gt=0)
    total_pole_positions: Optional[int] = Field(None, ge=0)
    total_race_wins: Optional[int] = Field(None, ge=0)
    total_points_scored: Optional[float] = Field(None, ge=0)
    total_world_titles: Optional[int] = Field(None, ge=0)
    total_fastest_laps: Optional[int] = Field(None, ge=0)
    team: Optional[str] = None

    @validator('team')
    def team_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Team cannot be empty')
        return v.strip() if v else v 