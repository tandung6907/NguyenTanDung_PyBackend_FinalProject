import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from config.setting import (
    SECRET_KEY,
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES
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
