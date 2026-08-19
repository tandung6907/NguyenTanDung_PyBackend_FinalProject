from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ClubActivityCreate(BaseModel):
    club_id                     : int
    title                       : str
    description                 : str
    assignee_id                 : int
    status                      : str
    priority                    : str
    due_date                    : Optional[datetime] = None

class ClubActivityUpdate(BaseModel):
    club_id                     : int
    title                       : str
    description                 : str
    assignee_id                 : int
    status                      : str
    priority                    : str
    due_date                    : Optional[datetime] = None

class ClubActivityResponse(BaseModel):
    club_activities_id          : int
    club_id                     : int
    title                       : str
    description                 : str
    assignee_id                 : int
    status                      : str
    priority                    : str
    due_date                    : datetime
    created_at                  : datetime

    model_config = ConfigDict(from_attributes= True)