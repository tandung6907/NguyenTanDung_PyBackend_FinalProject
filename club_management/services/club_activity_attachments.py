"""
TIẾT 4 - NÂNG CAO (45): ATTACHMENT
Chỉ thành viên câu lạc bộ sở hữu hoạt động mới được xem/upload file đính kèm.
Việc kiểm tra loại/kích thước file thực hiện ở utils/file_upload.py.
"""
from fastapi import UploadFile
from sqlalchemy.orm import Session

from models.users import UserModel
from models.club_activity_attachments import ClubActivityAttachmentModel

from services.clubs import _require_member
from services.club_activities import _get_activity_or_404

from utils.file_upload import save_activity_attachment


def upload_attachment(
        db: Session,
        activity_id: int,
        file: UploadFile,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    _require_member(db, activity.club_id, current_user)

    saved = save_activity_attachment(activity_id, file)

    attachment = ClubActivityAttachmentModel(
        club_activities_id= activity_id,
        uploader_id= current_user.user_id,
        file_name= saved["file_name"],
        file_path= saved["file_path"],
        file_type= saved["file_type"],
        file_size= saved["file_size"]
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def list_attachments(
        db: Session,
        activity_id: int,
        current_user: UserModel
):
    activity = _get_activity_or_404(db, activity_id)
    _require_member(db, activity.club_id, current_user)

    return db.query(ClubActivityAttachmentModel).filter(
        ClubActivityAttachmentModel.club_activities_id == activity_id
    ).order_by(ClubActivityAttachmentModel.created_at.desc()).all()
