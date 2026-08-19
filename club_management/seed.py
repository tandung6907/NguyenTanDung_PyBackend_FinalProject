from database.database import SessionLocal
from models.users import UserModel
from models.club_activities import ClubActivityModel
from models.clubs import ClubModel
from untils.security import hash_password

def seed_users(db):
    admin = db.query(UserModel).filter(UserModel.email == "admin@gmail.com").first()

    if not admin:
        admin = UserModel(
            email= "admin@gmail.com",
            password_hash= hash_password("Admin@123"),
            full_name= "Admin",
            role= "ADMIN",
            is_active= True
        )

        db.add(admin)

    users = [
        UserModel(
            email= "teacher@gmail.com",
            password_hash= hash_password("Teacher@123"),
            full_name= "Teacher",
            role= "USER",
            is_active= True
        ),
        UserModel(
            email= "student@gmail.com",
            password_hash= hash_password("Student@123"),
            full_name= "Student",
            role= "USER",
            is_active= True
        )
    ]
    db.add_all(users)
    db.commit()

def seed_clubs(db):
    clubs = [
        ClubModel(
            name="IT Club",
            description="Câu lạc bộ công nghệ thông tin"
        ),
        ClubModel(
            name="English Club",
            description="Câu lạc bộ tiếng Anh"
        ),
        ClubModel(
            name="Football Club",
            description="Câu lạc bộ bóng đá"
        )
    ]

    db.add_all(clubs)
    db.commit()

def seed_club_activities(db):
    activities = [
        ClubActivityModel(
            club_id= 1,
            title= "Tổ chức workshop Python",
            description= "Chuẩn bị nội dung và phòng học",
            assignee_id= 3,
            status= "pending",
            priority= "high"
        ),
        ClubActivityModel(
            club_id= 1,
            title= "Họp ban chủ nhiệm",
            description= "Họp phân công công việc",
            assignee_id= 2,
            status= "completed",
            priority= "medium"
        ),
        ClubActivityModel(
            club_id= 2,
            title= "English Speaking",
            description= "Tổ chức buổi luyện nói tiếng Anh",
            assignee_id= 3,
            status= "pending",
            priority= "low"
        )
    ]

    db.add_all(activities)
    db.commit()

def seed():
    db = SessionLocal()

    try:
        seed_users(db)
        seed_clubs(db)
        seed_club_activities(db)

        print("Seed data successfully")
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
    finally:
        db.close()