from database.database import SessionLocal

from models.users import UserModel
from models.clubs import ClubModel
from models.club_members import ClubMemberModel
from models.club_activities import ClubActivityModel
from models.club_logs import ClubLogModel

from utils.security import hash_password


def seed_users(db):
    users_data = [
        {
            "email": "admin@gmail.com",
            "password": "Admin@123",
            "full_name": "Admin",
            "role": "ADMIN",
            "is_active": True
        },
        {
            "email": "teacher@gmail.com",
            "password": "Teacher@123",
            "full_name": "Teacher",
            "role": "USER",
            "is_active": True
        },
        {
            "email": "student@gmail.com",
            "password": "Student@123",
            "full_name": "Student",
            "role": "USER",
            "is_active": True
        }
    ]

    users = {}

    for data in users_data:
        user = db.query(UserModel).filter(
            UserModel.email == data["email"]
        ).first()

        if not user:
            user = UserModel(
                email=data["email"],
                password_hash=hash_password(data["password"]),
                full_name=data["full_name"],
                role=data["role"],
                is_active=data["is_active"]
            )

            db.add(user)
            db.flush()

        users[data["email"]] = user

    return users


def seed_clubs(db, users):
    clubs_data = [
        {
            "name": "IT Club",
            "description": "Câu lạc bộ công nghệ thông tin",
            "owner_email": "admin@gmail.com"
        },
        {
            "name": "English Club",
            "description": "Câu lạc bộ tiếng Anh",
            "owner_email": "teacher@gmail.com"
        },
        {
            "name": "Football Club",
            "description": "Câu lạc bộ bóng đá",
            "owner_email": "student@gmail.com"
        }
    ]

    clubs = {}

    for data in clubs_data:
        owner = users[data["owner_email"]]

        club = db.query(ClubModel).filter(
            ClubModel.name == data["name"],
            ClubModel.is_deleted == False
        ).first()

        if not club:
            club = ClubModel(
                name=data["name"],
                description=data["description"],
                owner_id=owner.user_id,
                is_deleted=False,
                deleted_at=None
            )

            db.add(club)
            db.flush()

        clubs[data["name"]] = club

        membership = db.query(ClubMemberModel).filter(
            ClubMemberModel.club_id == club.club_id,
            ClubMemberModel.user_id == owner.user_id
        ).first()

        if not membership:
            membership = ClubMemberModel(
                club_id=club.club_id,
                user_id=owner.user_id,
                role="OWNER"
            )

            db.add(membership)

    return clubs


def seed_club_members(db, users, clubs):
    members_data = [
        {
            "club_name": "IT Club",
            "email": "teacher@gmail.com",
            "role": "MEMBER"
        },
        {
            "club_name": "IT Club",
            "email": "student@gmail.com",
            "role": "MEMBER"
        },
        {
            "club_name": "English Club",
            "email": "student@gmail.com",
            "role": "MEMBER"
        },
        {
            "club_name": "Football Club",
            "email": "teacher@gmail.com",
            "role": "MEMBER"
        }
    ]

    for data in members_data:
        club = clubs[data["club_name"]]
        user = users[data["email"]]

        existed = db.query(ClubMemberModel).filter(
            ClubMemberModel.club_id == club.club_id,
            ClubMemberModel.user_id == user.user_id
        ).first()

        if not existed:
            membership = ClubMemberModel(
                club_id=club.club_id,
                user_id=user.user_id,
                role=data["role"]
            )

            db.add(membership)


def seed_club_activities(db, users, clubs):
    activities_data = [
        {
            "club_name": "IT Club",
            "title": "Tổ chức workshop Python",
            "description": "Chuẩn bị nội dung và phòng học",
            "assignee_email": "student@gmail.com",
            "status": "TODO",
            "priority": "LOW"
        },
        {
            "club_name": "IT Club",
            "title": "Họp ban chủ nhiệm",
            "description": "Họp phân công công việc",
            "assignee_email": "teacher@gmail.com",
            "status": "IN_PROGRESS",
            "priority": "MEDIUM"
        },
        {
            "club_name": "English Club",
            "title": "English Speaking",
            "description": "Tổ chức buổi luyện nói tiếng Anh",
            "assignee_email": "student@gmail.com",
            "status": "DONE",
            "priority": "HIGH"
        }
    ]

    for data in activities_data:
        club = clubs[data["club_name"]]
        assignee = users[data["assignee_email"]]

        existed = db.query(ClubActivityModel).filter(
            ClubActivityModel.club_id == club.club_id,
            ClubActivityModel.title == data["title"]
        ).first()

        if not existed:
            activity = ClubActivityModel(
                club_id=club.club_id,
                title=data["title"],
                description=data["description"],
                assignee_id=assignee.user_id,
                status=data["status"],
                priority=data["priority"]
            )

            db.add(activity)


def seed():
    db = SessionLocal()

    try:
        users = seed_users(db)
        clubs = seed_clubs(db, users)
        seed_club_members(db, users, clubs)
        seed_club_activities(db, users, clubs)

        db.commit()

        print("Seed data successfully")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()