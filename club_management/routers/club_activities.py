"""
TIẾT 4: HOẠT ĐỘNG CÂU LẠC BỘ - các endpoint theo yêu cầu đề bài (mục 34-45)
"""
from typing import Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from sqlalchemy.orm import Session

from database.database import get_db
from models.users import UserModel

from schemas.club_activities import (
    ClubActivityCreate,
    ClubActivityUpdate,
    ClubActivityResponse,
    ClubActivityListResponse
)
from schemas.club_activity_comments import (
    ClubActivityCommentCreate,
    ClubActivityCommentResponse
)
from schemas.club_activity_attachments import ClubActivityAttachmentResponse

from services.club_activities import (
    create_activity,
    list_activities,
    get_activity_detail,
    update_activity,
    delete_activity
)
from services.club_activity_comments import create_comment, list_comments
from services.club_activity_attachments import upload_attachment, list_attachments

from utils.dependencies import get_current_user

activity_router = APIRouter(tags= ["Club Activities"])


# 34 - Tạo hoạt động câu lạc bộ
@activity_router.post(
    "/clubs/{club_id}/activities",
    response_model= ClubActivityResponse,
    status_code= status.HTTP_201_CREATED
)
def create_activity_api(
    club_id: int,
    data: ClubActivityCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return create_activity(
        db= db,
        club_id= club_id,
        data= data,
        current_user= current_user
    )


# 35 - Danh sách hoạt động câu lạc bộ (41 search & filter, 42 pagination & sort)
@activity_router.get(
    "/clubs/{club_id}/activities",
    response_model= ClubActivityListResponse
)
def list_activities_api(
    club_id: int,
    status: Optional[str] = Query(None, description= "TODO | IN_PROGRESS | DONE"),
    priority: Optional[str] = Query(None, description= "LOW | MEDIUM | HIGH"),
    assignee_id: Optional[int] = None,
    search: Optional[str] = Query(None, description= "Search by title"),
    page: int = Query(1, ge= 1),
    size: int = Query(10, ge= 1, le= 100),
    sort_by: str = Query("created_at", description= "created_at | due_date"),
    order: str = Query("desc", description= "asc | desc"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return list_activities(
        db= db,
        club_id= club_id,
        current_user= current_user,
        status= status,
        priority= priority,
        assignee_id= assignee_id,
        search= search,
        page= page,
        size= size,
        sort_by= sort_by,
        order= order
    )


# 36 - Chi tiết hoạt động câu lạc bộ
@activity_router.get(
    "/activities/{activity_id}",
    response_model= ClubActivityResponse
)
def get_activity_detail_api(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_activity_detail(
        db= db,
        activity_id= activity_id,
        current_user= current_user
    )


# 37 - Cập nhật hoạt động câu lạc bộ (39 giao việc, 40 workflow)
@activity_router.patch(
    "/activities/{activity_id}",
    response_model= ClubActivityResponse
)
def update_activity_api(
    activity_id: int,
    data: ClubActivityUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return update_activity(
        db= db,
        activity_id= activity_id,
        data= data,
        current_user= current_user
    )


# 38 - Xóa hoạt động câu lạc bộ (43 permission matrix: chỉ OWNER)
@activity_router.delete(
    "/activities/{activity_id}",
    status_code= status.HTTP_204_NO_CONTENT
)
def delete_activity_api(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    delete_activity(
        db= db,
        activity_id= activity_id,
        current_user= current_user
    )

    return None


# 44 - Nâng cao: Comment
@activity_router.post(
    "/activities/{activity_id}/comments",
    response_model= ClubActivityCommentResponse,
    status_code= status.HTTP_201_CREATED
)
def create_comment_api(
    activity_id: int,
    data: ClubActivityCommentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return create_comment(
        db= db,
        activity_id= activity_id,
        data= data,
        current_user= current_user
    )


@activity_router.get(
    "/activities/{activity_id}/comments",
    response_model= list[ClubActivityCommentResponse]
)
def list_comments_api(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return list_comments(
        db= db,
        activity_id= activity_id,
        current_user= current_user
    )


# 45 - Nâng cao: Attachment
@activity_router.post(
    "/activities/{activity_id}/attachments",
    response_model= ClubActivityAttachmentResponse,
    status_code= status.HTTP_201_CREATED
)
def upload_attachment_api(
    activity_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return upload_attachment(
        db= db,
        activity_id= activity_id,
        file= file,
        current_user= current_user
    )


@activity_router.get(
    "/activities/{activity_id}/attachments",
    response_model= list[ClubActivityAttachmentResponse]
)
def list_attachments_api(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return list_attachments(
        db= db,
        activity_id= activity_id,
        current_user= current_user
    )
