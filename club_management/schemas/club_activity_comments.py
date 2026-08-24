"""
TIẾT 4 - NÂNG CAO (44): COMMENT
Schema tạo/trả về bình luận trao đổi trong một hoạt động câu lạc bộ.
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ClubActivityCommentCreate(BaseModel):
    content : str = Field(..., min_length= 1, max_length= 2000)


class ClubActivityCommentResponse(BaseModel):
    comment_id          : int
    club_activities_id  : int
    author_id           : int
    author_name         : str
    content              : str
    created_at            : datetime

    model_config = ConfigDict(from_attributes= True)
