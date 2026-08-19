from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email           : str
    full_name       : str
    role            : str
    is_active       : bool

class UserCreate(UserBase):
    password        : str

class UserUpdate(BaseModel):
    email           : Optional[str]     = None
    password        : Optional[str]     = None
    full_name       : Optional[str]     = None
    role            : Optional[str]     = None
    is_active       : Optional[bool]    = None

class UserResponse(UserBase):
    user_id         : int
    created_at      : datetime

    model_config = ConfigDict(from_attributes= True)
