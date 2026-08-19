from fastapi import APIRouter, Depends
from models.users import UserModel
from schemas.users import UserResponse
from utils.dependencies import (
    get_current_user,
    require_admin
)
from typing import (
    List,
    Optional
)
from sqlalchemy.orm import Session
from database.database import get_db

user_router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)

@user_router.get("/me", response_model= UserResponse)
def get_profile(
    current_user: UserModel = Depends(get_current_user) 
): 
    return current_user

@user_router.get("/", response_model= List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_admin),
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    query = db.query(UserModel)

    if search:
        query = query.filter(
            (UserModel.email.like(f"%{search}%")) |
            (UserModel.full_name.like(f"%{search}%"))
        )

    if is_active is not None:
        query = query.filter(
            UserModel.is_active == is_active
        )

    return query.all()