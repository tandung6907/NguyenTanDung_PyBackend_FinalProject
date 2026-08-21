from fastapi import Header, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.users import UserModel
from utils.jwt import verify_token
from exceptions.custom import (
    UnauthorizedException,
    ForbiddenException
)


def get_current_user(
    authorization: str | None = Header(
        default=None,
        alias="Authorization"
    ),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise UnauthorizedException(
            "Authorization header is required"
        )

    parts = authorization.split(" ", 1)

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthorizedException(
            "Invalid authorization header"
        )

    token = parts[1].strip()

    if not token:
        raise UnauthorizedException(
            "Token is required"
        )

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

    user = db.query(UserModel).filter(
        UserModel.user_id == user_id
    ).first()

    if not user:
        raise UnauthorizedException(
            "User not found"
        )

    if not user.is_active:
        raise ForbiddenException(
            "User account is inactive"
        )

    return user


def role_check(*allowed_roles: str):
    def checker(
        current_user: UserModel = Depends(get_current_user)
    ):
        user_role = current_user.role

        if user_role not in allowed_roles:
            raise ForbiddenException(
                "You do not have permission to access this resource"
            )

        return current_user

    return checker


def require_admin(
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise ForbiddenException(
            "Admin permission required"
        )

    return current_user
