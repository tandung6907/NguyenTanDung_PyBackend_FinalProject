"""
TIẾT 4: HOẠT ĐỘNG CÂU LẠC BỘ (mục 34-43)

- 34 Tạo hoạt động: mọi thành viên câu lạc bộ được tạo.
- 35 Danh sách hoạt động theo club, không lộ hoạt động của club khác.
- 36 Chi tiết hoạt động: chỉ thành viên thuộc club mới xem được.
- 37 Cập nhật hoạt động: PATCH, chỉ ghi đè trường thực sự gửi lên.
- 38 Xóa hoạt động: chỉ OWNER được xóa.
- 39 Giao việc: assignee bắt buộc là thành viên đang sinh hoạt trong club.
- 40 Workflow: validate chuyển trạng thái status + priority hợp lệ.
- 41 Search & filter: kết hợp status/priority/assignee/title.
- 42 Pagination & sort: page/size + sort theo created_at/due_date.
- 43 Permission matrix: OWNER toàn quyền; ASSIGNEE chỉ được đổi status;
     MEMBER thường chỉ được xem, không được sửa/xóa.
"""
from typing import Optional

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from models.club_activities import ClubActivityModel
from models.users import UserModel

from schemas.club_activities import ClubActivityCreate, ClubActivityUpdate

from services.clubs import (
    _get_club_or_404,
    _get_membership,
    _require_member,
    _require_owner,
    _log
)

from exceptions.custom import (
    NotFoundException,
    ForbiddenException,
    BadRequestException
)

VALID_STATUS_TRANSITIONS = {
    "TODO"          : {"TODO", "IN_PROGRESS"},
    "IN_PROGRESS"   : {"IN_PROGRESS", "TODO", "DONE"},
    "DONE"          : {"DONE", "IN_PROGRESS"}
}

SORTABLE_FIELDS = {
    "created_at"    : ClubActivityModel.created_at,
    "due_date"      : ClubActivityModel.due_date
}


def _get_activity_or_404(db: Session, activity_id: int) -> ClubActivityModel:
    activity = db.query(ClubActivityModel).filter(
        ClubActivityModel.club_activities_id == activity_id
    ).first()

    if not activity:
        raise NotFoundException("Activity not found")

    return activity


def _validate_assignee_is_member(db: Session, club_id: int, assignee_id: int):
    membership = _get_membership(db, club_id, assignee_id)

    if not membership:
        raise BadRequestException(
            "Assignee must be an active member of this club"
        )


def _validate_status_transition(current_status: str, new_status: str):
    allowed = VALID_STATUS_TRANSITIONS.get(current_status, set())

    if new_status not in allowed:
        raise BadRequestException(
            f"Cannot transition status from '{current_status}' to '{new_status}'"
        )


def create_activity(
        db: Session,
        club_id: int,
        data: ClubActivityCreate,
        current_user: UserModel
):
    _get_club_or_404(db, club_id)
    _require_member(db, club_id, current_user)

    assignee_id = data.assignee_id
    if assignee_id is None:
        assignee_id = current_user.user_id
    else:
        _validate_assignee_is_member(db, club_id, data.assignee_id)
    
    activity = ClubActivityModel(
        club_id= club_id,
        title= data.title,
        description= data.description,
        assignee_id= assignee_id,
        status= "TODO",
        priority= data.priority,
        due_date= data.due_date
    )

    db.add(activity)
    db.flush()

    _log(
        db,
        club_id= club_id,
        actor_id= current_user.user_id,
        action= "CREATE_ACTIVITY",
        detail= f"Created activity '{activity.title}'"
    )

    db.commit()
    db.refresh(activity)

    return activity


def list_activities(
        db: Session,
        club_id: int,
        current_user: UserModel,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        size: int = 10,
        sort_by: str = "created_at",
        order: str = "desc"
):
    _get_club_or_404(db, club_id)
    _require_member(db, club_id, current_user)

    query = db.query(ClubActivityModel).filter(
        ClubActivityModel.club_id == club_id
    )

    if status:
        query = query.filter(ClubActivityModel.status == status)

    if priority:
        query = query.filter(ClubActivityModel.priority == priority)

    if assignee_id:
        query = query.filter(ClubActivityModel.assignee_id == assignee_id)

    if search:
        query = query.filter(ClubActivityModel.title.like(f"%{search}%"))

    total_activities = query.count()

    sort_column = SORTABLE_FIELDS.get(sort_by, ClubActivityModel.created_at)
    query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    page = max(page, 1)
    size = max(min(size, 100), 1)

    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items"             : items,
        "total_activities"  : total_activities,
        "page"              : page,
        "size"              : size
    }


def get_activity_detail(
        db: Session,
        activity_id: int,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    _require_member(db, activity.club_id, current_user)

    return activity


def update_activity(
        db: Session,
        activity_id: int,
        data: ClubActivityUpdate,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    membership = _require_member(db, activity.club_id, current_user)

    update_data = data.model_dump(exclude_unset= True)

    is_owner = membership.role == "OWNER"
    is_assignee = activity.assignee_id == current_user.user_id

    if not is_owner and not is_assignee:
        raise ForbiddenException(
            "Only the club owner or the assignee can update this activity"
        )

    if not is_owner:
        not_allowed_fields = set(update_data.keys()) - {"status"}

        if not_allowed_fields:
            raise ForbiddenException(
                "Only the club owner can update fields other than status"
            )

    if "assignee_id" in update_data and update_data["assignee_id"] != activity.assignee_id:
        _validate_assignee_is_member(db, activity.club_id, update_data["assignee_id"])

    if "status" in update_data and update_data["status"] != activity.status:
        _validate_status_transition(activity.status, update_data["status"])

    for field, value in update_data.items():
        setattr(activity, field, value)

    _log(
        db,
        club_id= activity.club_id,
        actor_id= current_user.user_id,
        action= "UPDATE_ACTIVITY",
        detail= f"Updated fields: {', '.join(update_data.keys())}" if update_data else "No changes"
    )

    db.commit()
    db.refresh(activity)

    return activity


def delete_activity(
        db: Session,
        activity_id: int,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    _require_owner(db, activity.club_id, current_user)

    club_id = activity.club_id
    title = activity.title

    db.delete(activity)

    _log(
        db,
        club_id= club_id,
        actor_id= current_user.user_id,
        action= "DELETE_ACTIVITY",
        detail= f"Deleted activity '{title}'"
    )

    db.commit()

    return None
