from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email           : str
    password        : str   
    full_name       : str
    role            : str
    is_active       : bool

class UserUpdate(BaseModel):
    email           : Optional[str]     = None
    password        : Optional[str]     = None   
    full_name       : Optional[str]     = None
    role            : Optional[str]     = None
    is_active       : Optional[bool]    = None

class UserResponse(BaseModel):
    user_id         : int
    email           : str
    full_name       : str
    role            : str
    is_active       : bool
    created_at      : datetime

    model_config = ConfigDict(from_attributes= True)