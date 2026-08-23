from database.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ClubLogModel(Base):
    __tablename__ = "club_logs"

    log_id          = Column(Integer, primary_key= True, autoincrement= True)
    club_id         = Column(Integer, ForeignKey("clubs.club_id"), nullable= False)
    actor_id        = Column(Integer, ForeignKey("users.user_id"), nullable= False)
    action          = Column(String(50), nullable= False)
    detail          = Column(Text, default= None)
    created_at      = Column(DateTime, default= datetime.now, nullable= False)

    club    = relationship("ClubModel", back_populates= "logs")
    actor   = relationship("UserModel", back_populates= "club_logs")
