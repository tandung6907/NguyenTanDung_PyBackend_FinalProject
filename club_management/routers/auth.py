from fastapi import APIRouter, Depends
from database.database import get_db
from sqlalchemy.orm import Session
from models.users import UserModel
from schemas.users import (
    UserCreate, 
    UserResponse, 
    UserLogin
)
from utils.security import (
    hash_password, 
    verify_password
)
from utils.jwt import create_access_token
from exceptions.custom import (
    ConflictException, 
    UnauthorizedException, 
    ForbiddenException
)

auth_router = APIRouter(
    prefix= "/auth",
    tags= ["Authentication"]
)

@auth_router.post("/register", response_model= UserResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    email_existed = db.query(UserModel).filter(UserModel.email == data.email).first()

    if email_existed:
        raise ConflictException(
            "Email already exists"
        )

    user = UserModel(
        email= data.email,
        password_hash= hash_password(data.password),
        full_name= data.full_name,
        role= "USER",
        is_active= True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@auth_router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if not user:
        raise UnauthorizedException(
            "Email or password is incorrect"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise UnauthorizedException(
            "Email or password is incorrect"
        )

    if not user.is_active:
        raise ForbiddenException(
            "User account is inactive"
        )

    token = create_access_token({
        "sub"       : user.email,
        "user_id"   : user.user_id,
        "role"      : user.role
    })

    return {
        "access_token"  : token,
        "token_type"    : "bearer"
    }
