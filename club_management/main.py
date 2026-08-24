from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from database.database import Base, engine

from models.club_activities import ClubActivityModel
from models.club_activity_comments import ClubActivityCommentModel
from models.club_activity_attachments import ClubActivityAttachmentModel
from models.club_members import ClubMemberModel
from models.club_logs import ClubLogModel
from models.clubs import ClubModel
from models.users import UserModel

from routers.health_check import health_router
from routers.users import user_router
from routers.auth import auth_router
from routers.clubs import club_router
from routers.club_activities import activity_router

from exceptions.custom import AppException
from exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

app = FastAPI()

app.include_router(health_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(club_router)
app.include_router(activity_router)

app.add_exception_handler(
    AppException,
    app_exception_handler,
    
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)
app.add_exception_handler(
    Exception,
    general_exception_handler
)

Base.metadata.create_all(bind= engine)

@app.get("/")
def home():
    return {"message" : "Chào mừng đến với API của TanDung"}

