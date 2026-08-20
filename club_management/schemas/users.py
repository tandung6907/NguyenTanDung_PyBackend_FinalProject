from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email           : EmailStr
    full_name       : str


class UserCreate(UserBase):
    password        : str

class UserUpdate(BaseModel):
    email           : Optional[EmailStr] = None
    password        : Optional[str]     = None
    full_name       : Optional[str]     = None
    role            : Optional[str]     = None
    is_active       : Optional[bool]    = None

class UserResponse(UserBase):
    user_id         : int
    created_at      : datetime
    role            : str
    is_active       : bool

    model_config = ConfigDict(from_attributes= True)

class UserLogin(BaseModel):
    email           : EmailStr
    password        : str

class TokenResponse(BaseModel):
    access_token    : str
    refresh_token   : str
    token_type      : str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token   : str