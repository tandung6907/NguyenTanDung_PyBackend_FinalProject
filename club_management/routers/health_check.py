from fastapi import APIRouter, Depends
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

health_router = APIRouter(
    prefix= "/health",
    tags= ["Health"]
)

@health_router.get("")
def health_check_api(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status"    : "ok",
            "database"  : "connected"
        }

    except Exception:
        return {
            "status"    : "error",
            "database"  : "disconnected"
        }

