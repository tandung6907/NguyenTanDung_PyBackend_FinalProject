from fastapi import FastAPI
from database.database import Base, engine

from models.club_activities import ClubActivityModel
from models.club_members import ClubMemberModel
from models.clubs import ClubModel
from models.users import UserModel

from routers.health_check import health_router
from routers.users import user_router
from routers.auth import auth_router

from exceptions.custom import AppException
from exceptions.handlers import app_exception_handler

app = FastAPI()

app.include_router(health_router)
app.include_router(user_router)
app.include_router(auth_router)

app.add_exception_handler(
    AppException,
    app_exception_handler
)

Base.metadata.create_all(bind= engine)

@app.get("/")
def home():
    return {"message" : "Chào mừng đến với API của TanDung"}

