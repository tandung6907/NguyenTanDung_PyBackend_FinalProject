import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from config.setting import (
    SECRET_KEY,
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    REFRESH_SECRET_KEY,
    REFRESH_EXPIRE_DAYS
)

def create_access_token(data: dict) -> str:
    payload = data.copy()

    expired_time = datetime.now(timezone.utc) + timedelta(
        minutes= JWT_EXPIRE_MINUTES
    )

    payload["exp"] = expired_time

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm= JWT_ALGORITHM
    )

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except ExpiredSignatureError:
        raise ValueError("Token has expired")

    except InvalidTokenError:
        raise ValueError("Invalid token")

def create_refresh_token(data: dict) -> str:
    payload = data.copy()

    expired_time = datetime.now(timezone.utc) + timedelta(
        days= REFRESH_EXPIRE_DAYS
    )

    payload["exp"] = expired_time
    payload["type"] = "refresh"

    return jwt.encode(
        payload,
        REFRESH_SECRET_KEY,
        algorithm= JWT_ALGORITHM
    )

def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            REFRESH_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        return payload

    except ExpiredSignatureError:
        raise ValueError("Refresh token has expired")

    except InvalidTokenError:
        raise ValueError("Invalid refresh token")
