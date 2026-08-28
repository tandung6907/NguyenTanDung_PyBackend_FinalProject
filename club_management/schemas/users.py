from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email           : EmailStr
    # Chuẩn hóa email thành chữ thường và loại bỏ khoảng trắng trước khi lưu vào database.
    @field_validator("email")
    @classmethod
    def validation(cls, value):
        value.lower().strip()

        if not value:
            raise ValueError("Email cannot be empty")

        return value

    full_name       : str = Field(min_length= 2)


class UserCreate(UserBase):
    password        : str = Field(min_length= 8)

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