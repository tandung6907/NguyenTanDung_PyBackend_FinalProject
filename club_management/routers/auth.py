from fastapi import APIRouter, Depends, Request
from database.database import get_db
from sqlalchemy.orm import Session
from models.users import UserModel
from schemas.users import (
    UserCreate, 
    UserResponse, 
    UserLogin,
    TokenResponse,
    RefreshTokenRequest
)
from utils.security import (
    hash_password, 
    verify_password
)
from utils.jwt import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from utils.rate_limiter import check_login_rate_limit
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

@auth_router.post("/login", response_model= TokenResponse)
def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    check_login_rate_limit(request.client.host)

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

    token_payload = {
        "sub"       : user.email,
        "user_id"   : user.user_id,
        "role"      : user.role
    }

    return {
        "access_token"  : create_access_token(token_payload),
        "refresh_token" : create_refresh_token(token_payload),
        "token_type"    : "bearer"
    }

@auth_router.post("/refresh", response_model= TokenResponse)
def refresh_access_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = verify_refresh_token(data.refresh_token)
    except Exception:
        raise UnauthorizedException(
            "Invalid or expired refresh token"
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise UnauthorizedException(
            "Invalid refresh token"
        )

    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    if not user:
        raise UnauthorizedException(
            "User not found"
        )

    if not user.is_active:
        raise ForbiddenException(
            "User account is inactive"
        )

    token_payload = {
        "sub"       : user.email,
        "user_id"   : user.user_id,
        "role"      : user.role
    }

    return {
        "access_token"  : create_access_token(token_payload),
        "refresh_token" : create_refresh_token(token_payload),
        "token_type"    : "bearer"
    }
