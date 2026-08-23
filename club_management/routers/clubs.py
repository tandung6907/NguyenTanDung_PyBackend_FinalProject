from typing import List, Optional

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from database.database import get_db
from models.users import UserModel
from schemas.clubs import (
    ClubCreate,
    ClubUpdate,
    ClubResponse,
    ClubWithRoleResponse,
    AddMemberRequest
)
from schemas.club_members import ClubMemberResponse, ClubMemberDetailResponse
from services.clubs import (
    create_club,
    get_clubs_for_user,
    get_club_detail,
    update_club,
    delete_club,
    add_member,
    remove_member,
    list_members
)
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


@club_router.get("/", response_model= List[ClubWithRoleResponse])
def get_clubs_api(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_clubs_for_user(
        db= db,
        current_user= current_user,
        search= search
    )


@club_router.get("/{club_id}", response_model= ClubWithRoleResponse)
def get_club_detail_api(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_club_detail(
        db= db,
        club_id= club_id,
        current_user= current_user
    )


@club_router.put("/{club_id}", response_model= ClubResponse)
@club_router.patch("/{club_id}", response_model= ClubResponse)
def update_club_api(
    club_id: int,
    data: ClubUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return update_club(
        db= db,
        club_id= club_id,
        data= data,
        current_user= current_user
    )


@club_router.delete("/{club_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_club_api(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    delete_club(
        db= db,
        club_id= club_id,
        current_user= current_user
    )

    return None


@club_router.post("/{club_id}/members", response_model= ClubMemberResponse)
def add_member_api(
    club_id: int,
    data: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return add_member(
        db= db,
        club_id= club_id,
        data= data,
        current_user= current_user
    )


@club_router.delete("/{club_id}/members/{user_id}", status_code= status.HTTP_204_NO_CONTENT)
def remove_member_api(
    club_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    remove_member(
        db= db,
        club_id= club_id,
        user_id= user_id,
        current_user= current_user
    )

    return None


@club_router.get("/{club_id}/members", response_model= List[ClubMemberDetailResponse])
def list_members_api(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return list_members(
        db= db,
        club_id= club_id,
        current_user= current_user
    )
