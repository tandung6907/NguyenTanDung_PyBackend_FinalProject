from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ClubBase(BaseModel):
    name            : str
    description     : Optional[str] = None
    owner_id        : int

class ClubCreate(ClubBase):
    pass

class ClubUpdate(BaseModel):
    name            : Optional[str] = None
    description     : Optional[str] = None
    owner_id        : Optional[int] = None

class ClubResponse(ClubBase):
    club_id         : int
    created_at      : datetime

    model_config = ConfigDict(from_attributes= True)
