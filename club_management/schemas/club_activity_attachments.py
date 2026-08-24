"""
TIẾT 4 - NÂNG CAO (45): ATTACHMENT
Schema trả về thông tin file đính kèm (minh chứng, hình ảnh) của một hoạt động.
Việc upload dùng multipart/form-data nên không cần schema request riêng.
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ClubActivityAttachmentResponse(BaseModel):
    attachment_id        : int
    club_activities_id   : int
    uploader_id            : int
    file_name               : str
    file_type                : str
    file_size                 : int
    created_at                  : datetime

    model_config = ConfigDict(from_attributes= True)
