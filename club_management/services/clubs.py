from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from models.clubs import ClubModel
from models.club_members import ClubMemberModel
from models.club_logs import ClubLogModel
from models.users import UserModel

from schemas.clubs import ClubCreate, ClubUpdate, AddMemberRequest

from exceptions.custom import (
    NotFoundException,
    ForbiddenException,
    ConflictException,
    BadRequestException
)


def _log(db: Session, club_id: int, actor_id: int, action: str, detail: str = None):
    log = ClubLogModel(
        club_id= club_id,
        actor_id= actor_id,
        action= action,
        detail= detail
    )

    db.add(log)


def _get_club_or_404(db: Session, club_id: int) -> ClubModel:
    club = db.query(ClubModel).filter(
        ClubModel.club_id == club_id,
        ClubModel.is_deleted == False
    ).first()

    if not club:
        raise NotFoundException("Club not found")

    return club


def _get_membership(db: Session, club_id: int, user_id: int) -> Optional[ClubMemberModel]:
    return db.query(ClubMemberModel).filter(
        ClubMemberModel.club_id == club_id,
        ClubMemberModel.user_id == user_id
    ).first()


def _require_owner(db: Session, club_id: int, current_user: UserModel) -> ClubMemberModel:
    membership = _get_membership(db, club_id, current_user.user_id)

    if not membership or membership.role != "OWNER":
        raise ForbiddenException("Only the club owner can perform this action")

    return membership


def _require_member(db: Session, club_id: int, current_user: UserModel) -> ClubMemberModel:
    membership = _get_membership(db, club_id, current_user.user_id)

    if not membership:
        raise ForbiddenException("You are not a member of this club")

    return membership


def create_club(
        data: ClubCreate,
        db: Session,
        current_user: UserModel
):
    club = ClubModel(
        name= data.name,
        description= data.description,
        owner_id= current_user.user_id
    )

    db.add(club)
    db.flush()

    member = ClubMemberModel(
        club_id= club.club_id,
        user_id= current_user.user_id,
        role= "OWNER"
    )

    db.add(member)

    _log(
        db,
        club_id= club.club_id,
        actor_id= current_user.user_id,
        action= "CREATE_CLUB",
        detail= f"Created club '{club.name}'"
    )

    db.commit()
    db.refresh(club)

    return club


def get_clubs_for_user(
        db: Session,
        current_user: UserModel,
        search: Optional[str] = None
):
    query = db.query(ClubModel).join(
        ClubMemberModel,
        ClubMemberModel.club_id == ClubModel.club_id
    ).filter(
        ClubMemberModel.user_id == current_user.user_id,
        ClubModel.is_deleted == False
    )

    if search:
        query = query.filter(
            ClubModel.name.like(f"%{search}%")
        )

    clubs = query.all()

    results = []

    for club in clubs:
        membership = _get_membership(db, club.club_id, current_user.user_id)

        results.append({
            "club_id"       : club.club_id,
            "name"          : club.name,
            "description"   : club.description,
            "owner_id"      : club.owner_id,
            "created_at"    : club.created_at,
            "role"          : membership.role
        })

    return results


def get_club_detail(
        db: Session,
        club_id: int,
        current_user: UserModel
):
    club = _get_club_or_404(db, club_id)
    membership = _require_member(db, club_id, current_user)

    return {
        "club_id"       : club.club_id,
        "name"          : club.name,
        "description"   : club.description,
        "owner_id"      : club.owner_id,
        "created_at"    : club.created_at,
        "role"          : membership.role
    }


def update_club(
        db: Session,
        club_id: int,
        data: ClubUpdate,
        current_user: UserModel
):
    club = _get_club_or_404(db, club_id)
    _require_owner(db, club_id, current_user)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(club, field, value)

    _log(
        db,
        club_id= club.club_id,
        actor_id= current_user.user_id,
        action= "UPDATE_CLUB",
        detail= f"Updated fields: {', '.join(update_data.keys())}" if update_data else "No changes"
    )

    db.commit()
    db.refresh(club)

    return club


def delete_club(
        db: Session,
        club_id: int,
        current_user: UserModel
):
    club = _get_club_or_404(db, club_id)
    _require_owner(db, club_id, current_user)

    club.is_deleted = True
    club.deleted_at = datetime.now()

    _log(
        db,
        club_id= club.club_id,
        actor_id= current_user.user_id,
        action= "DELETE_CLUB",
        detail= f"Deleted club '{club.name}'"
    )

    db.commit()

    return None


def add_member(
        db: Session,
        club_id: int,
        data: AddMemberRequest,
        current_user: UserModel
):
    _get_club_or_404(db, club_id)
    _require_owner(db, club_id, current_user)

    target_user = db.query(UserModel).filter(
        UserModel.user_id == data.user_id
    ).first()

    if not target_user:
        raise NotFoundException("User not found")

    existing_membership = _get_membership(db, club_id, data.user_id)

    if existing_membership:
        raise ConflictException("User is already a member of this club")

    member = ClubMemberModel(
        club_id= club_id,
        user_id= data.user_id,
        role= "MEMBER"
    )

    db.add(member)

    _log(
        db,
        club_id= club_id,
        actor_id= current_user.user_id,
        action= "ADD_MEMBER",
        detail= f"Added user_id={data.user_id} as MEMBER"
    )

    db.commit()
    db.refresh(member)

    return member


def remove_member(
        db: Session,
        club_id: int,
        user_id: int,
        current_user: UserModel
):
    _get_club_or_404(db, club_id)
    _require_owner(db, club_id, current_user)

    membership = _get_membership(db, club_id, user_id)

    if not membership:
        raise NotFoundException("Member not found in this club")

    if membership.role == "OWNER":
        owner_count = db.query(ClubMemberModel).filter(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.role == "OWNER"
        ).count()

        if owner_count <= 1:
            raise BadRequestException("Cannot remove the last owner of the club")

    db.delete(membership)

    _log(
        db,
        club_id= club_id,
        actor_id= current_user.user_id,
        action= "REMOVE_MEMBER",
        detail= f"Removed user_id={user_id} from club"
    )

    db.commit()

    return None


def list_members(
        db: Session,
        club_id: int,
        current_user: UserModel
):
    _get_club_or_404(db, club_id)
    _require_member(db, club_id, current_user)

    memberships = db.query(ClubMemberModel).options(
        joinedload(ClubMemberModel.user)
    ).filter(
        ClubMemberModel.club_id == club_id
    ).all()

    results = []

    for membership in memberships:
        results.append({
            "user_id"       : membership.user_id,
            "email"         : membership.user.email,
            "full_name"     : membership.user.full_name,
            "role"          : membership.role,
            "joined_at"     : membership.joined_at
        })

    return results
