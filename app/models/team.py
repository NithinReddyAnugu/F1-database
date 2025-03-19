from pydantic import BaseModel, Field, validator
from typing import Optional

class Team(BaseModel):
    """
    Model representing a Formula 1 team
    """
    name: str
    year_founded: int = Field(..., gt=1900, lt=2100)
    total_pole_positions: int = Field(..., ge=0)
    total_race_wins: int = Field(..., ge=0)
    total_constructor_titles: int = Field(..., ge=0)
    finishing_position_previous_season: int = Field(..., gt=0)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class TeamUpdate(BaseModel):
    """
    Model for updating a team's information
    """
    year_founded: Optional[int] = Field(None, gt=1900, lt=2100)
    total_pole_positions: Optional[int] = Field(None, ge=0)
    total_race_wins: Optional[int] = Field(None, ge=0)
    total_constructor_titles: Optional[int] = Field(None, ge=0)
    finishing_position_previous_season: Optional[int] = Field(None, gt=0) 