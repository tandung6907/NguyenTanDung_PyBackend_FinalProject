import jwt
from fastapi import (
    Depends, 
    HTTPException, 
    status
)
from fastapi.security import (
    HTTPAuthorizationCredentials, 
    HTTPBearer
)
from sqlalchemy.orm import Session
from config.setting import (
    SECRET_KEY, 
    JWT_ALGORITHM
)
from database.database import get_db
from models.users import UserModel
from exceptions.custom import ForbiddenException

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing subject"
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid subject"
        )

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
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
