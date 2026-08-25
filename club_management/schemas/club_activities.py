"""
TIẾT 4: HOẠT ĐỘNG CÂU LẠC BỘ
Schema cho các thao tác CRUD hoạt động, workflow status/priority (mục 40),
và danh sách có phân trang/sort (mục 42).
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal, Optional
from datetime import datetime

ActivityStatus = Literal["TODO", "IN_PROGRESS", "DONE"]
ActivityPriority = Literal["LOW", "MEDIUM", "HIGH"]


class ClubActivityCreate(BaseModel):
    title           : str = Field(..., min_length= 1, max_length= 255)
    description     : Optional[str] = None
    assignee_id     : int = Field(..., gt= 0)
    priority        : ActivityPriority = "MEDIUM"
    due_date        : Optional[datetime] = None


class ClubActivityUpdate(BaseModel):
    title           : Optional[str] = Field(None, min_length= 1, max_length= 255)
    description     : Optional[str] = None
    assignee_id     : Optional[int] = Field(None, gt= 0)
    status          : Optional[ActivityStatus] = None
    priority        : Optional[ActivityPriority] = None
    due_date        : Optional[datetime] = None


class ClubActivityResponse(BaseModel):
    club_activities_id  : int
    club_id             : int
    title               : str
    description         : Optional[str] = None
    assignee_id         : int
    status              : str
    priority            : str
    due_date            : Optional[datetime] = None
    created_at          : datetime

    model_config = ConfigDict(from_attributes= True)


class ClubActivityListResponse(BaseModel):
    items       : List[ClubActivityResponse]
    total       : int
    page        : int
    size        : int
