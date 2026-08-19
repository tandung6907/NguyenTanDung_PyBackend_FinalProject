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
    club_id                     : Optional[int] = None
    title                       : Optional[str] = None
    description                 : Optional[str] = None
    assignee_id                 : Optional[int] = None
    status                      : Optional[str] = None
    priority                    : Optional[str] = None
    due_date                    : Optional[datetime] = None

class ClubActivityResponse(BaseModel):
    club_activities_id          : int
    club_id                     : int
    title                       : str
    description                 : Optional[str] = None
    assignee_id                 : int
    status                      : str
    priority                    : str
    due_date                    : Optional[datetime] = None
    created_at                  : datetime

    model_config = ConfigDict(from_attributes= True)