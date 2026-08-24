"""
TIẾT 4 - NÂNG CAO (44): COMMENT
Model lưu các bình luận trao đổi trong ban chủ nhiệm/thành viên câu lạc bộ
gắn với một hoạt động câu lạc bộ (club activity) cụ thể.
"""
from database.database import Base
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ClubActivityCommentModel(Base):
    __tablename__ = "club_activity_comments"

    comment_id          = Column(Integer, primary_key= True, autoincrement= True)
    club_activities_id  = Column(Integer, ForeignKey("club_activities.club_activities_id"), nullable= False)
    author_id            = Column(Integer, ForeignKey("users.user_id"), nullable= False)
    content              = Column(Text, nullable= False)
    created_at           = Column(DateTime, default= datetime.now, nullable= False)

    activity    = relationship("ClubActivityModel", back_populates= "comments")
    author      = relationship("UserModel", back_populates= "activity_comments")
