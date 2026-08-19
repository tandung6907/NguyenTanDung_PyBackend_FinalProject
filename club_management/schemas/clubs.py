from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ClubCreate(BaseModel):
    name            : str
    description     : Optional[str] = None
    owner_id        : int

class ClubUpdate(BaseModel):
    name            : str
    description     : Optional[str] = None
    owner_id        : int

class ClubResponse(BaseModel):
    club_id         : int
    name            : str
    description     : Optional[str] = None
    owner_id        : int
    created_at      : datetime

    model_config = ConfigDict(from_attributes= True)