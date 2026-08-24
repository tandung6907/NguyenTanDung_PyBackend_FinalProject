"""
TIẾT 4 - NÂNG CAO (44): COMMENT
Chỉ thành viên câu lạc bộ sở hữu hoạt động mới được xem/tạo comment.
"""
from sqlalchemy.orm import Session, joinedload

from models.users import UserModel
from models.club_activity_comments import ClubActivityCommentModel

from schemas.club_activity_comments import ClubActivityCommentCreate

from services.clubs import _require_member
from services.club_activities import _get_activity_or_404


def create_comment(
        db: Session,
        activity_id: int,
        data: ClubActivityCommentCreate,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    _require_member(db, activity.club_id, current_user)

    comment = ClubActivityCommentModel(
        club_activities_id= activity_id,
        author_id= current_user.user_id,
        content= data.content
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {
        "comment_id"            : comment.comment_id,
        "club_activities_id"    : comment.club_activities_id,
        "author_id"             : comment.author_id,
        "author_name"           : current_user.full_name,
        "content"               : comment.content,
        "created_at"            : comment.created_at
    }


def list_comments(
        db: Session,
        activity_id: int,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    _require_member(db, activity.club_id, current_user)

    comments = db.query(ClubActivityCommentModel).options(
        joinedload(ClubActivityCommentModel.author)
    ).filter(
        ClubActivityCommentModel.club_activities_id == activity_id
    ).order_by(ClubActivityCommentModel.created_at.asc()).all()

    results = []

    for comment in comments:
        results.append({
            "comment_id"            : comment.comment_id,
            "club_activities_id"    : comment.club_activities_id,
            "author_id"             : comment.author_id,
            "author_name"           : comment.author.full_name,
            "content"               : comment.content,
            "created_at"            : comment.created_at
        })

    return results
