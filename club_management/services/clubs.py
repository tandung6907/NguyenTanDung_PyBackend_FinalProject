from sqlalchemy.orm import Session

from models.clubs import ClubModel
from models.club_members import ClubMemberModel
from models.users import UserModel

from schemas.clubs import ClubCreate

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

    db.commit()
    db.refresh(club)

    return club



