from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.database import get_db
from models.users import UserModel
from schemas.clubs import ClubCreate, ClubResponse
from services.clubs import create_club
from utils.dependencies import get_current_user

club_router = APIRouter(
    prefix= "/clubs",
    tags= ["Clubs"]
)

@club_router.post("/", response_model= ClubResponse)
def create_club_api(
    data: ClubCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return create_club(
        data= data,
        current_user= current_user,
        db= db
    )

