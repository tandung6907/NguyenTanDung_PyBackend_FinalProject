from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ClubMemberBase(BaseModel):
    club_id         : int
    user_id         : int
    role            : str

class ClubMemberCreate(ClubMemberBase):
    pass

class ClubMemberUpdate(BaseModel):
    role            : Optional[str] = None

class ClubMemberResponse(ClubMemberBase):
    joined_at       : datetime

    model_config = ConfigDict(from_attributes= True)


class ClubMemberDetailResponse(BaseModel):
    user_id         : int
    email           : str
    full_name       : str
    role            : str
    joined_at       : datetime

    model_config = ConfigDict(from_attributes= True)
