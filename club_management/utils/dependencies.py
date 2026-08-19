from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from models.users import UserModel
from utils.jwt import verify_token
from exceptions.custom import (
    UnauthorizedException,
    ForbiddenException
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl= "/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = verify_token(token)
    except Exception:
        raise UnauthorizedException(
            "Invalid or expired token"
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise UnauthorizedException(
            "Invalid token"
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

    return user
    
def require_admin(
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise ForbiddenException(
            "Admin permission required"
        )

    return current_user

