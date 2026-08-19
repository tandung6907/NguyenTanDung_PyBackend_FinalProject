from database.database import Base
from sqlalchemy import Column, Enum, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class ClubActivityModel(Base):
    __tablename__ = "club_activities"

    club_activities_id          = Column(Integer, primary_key= True, autoincrement= True)
    club_id                     = Column(Integer, ForeignKey("clubs.club_id"), nullable= False)
    title                       = Column(String(255), nullable= False)
    description                 = Column(Text, default= None)
    assignee_id                 = Column(Integer, ForeignKey("users.user_id"), nullable= False)
    status                      = Column(Enum("TODO", "IN_PROGRESS", "DONE"), nullable= False)
    priority                    = Column(Enum("LOW", "MEDIUM", "HIGH"), nullable= False)
    due_date                    = Column(DateTime, default= None)
    created_at                  = Column(DateTime, default= datetime.now, nullable= False)

    club        = relationship("ClubModel", back_populates= "activities")
    assignee    = relationship("UserModel", back_populates= "assigned_activities")
