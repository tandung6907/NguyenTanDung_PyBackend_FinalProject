"""
TIẾT 4 - NÂNG CAO (45): ATTACHMENT
Model lưu thông tin file đính kèm (minh chứng, hình ảnh hoạt động phong trào)
được upload cho một hoạt động câu lạc bộ. File vật lý được lưu trên ổ đĩa,
bảng này chỉ lưu đường dẫn và metadata.
"""
from database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ClubActivityAttachmentModel(Base):
    __tablename__ = "club_activity_attachments"

    attachment_id        = Column(Integer, primary_key= True, autoincrement= True)
    club_activities_id   = Column(Integer, ForeignKey("club_activities.club_activities_id"), nullable= False)
    uploader_id           = Column(Integer, ForeignKey("users.user_id"), nullable= False)
    file_name              = Column(String(255), nullable= False)
    file_path               = Column(String(500), nullable= False)
    file_type               = Column(String(100), nullable= False)
    file_size               = Column(Integer, nullable= False)
    created_at               = Column(DateTime, default= datetime.now, nullable= False)

    activity    = relationship("ClubActivityModel", back_populates= "attachments")
    uploader    = relationship("UserModel", back_populates= "activity_attachments")
