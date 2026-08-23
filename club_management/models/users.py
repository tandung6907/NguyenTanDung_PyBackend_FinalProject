from database.database import Base
from sqlalchemy import Column, String, Integer, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class UserModel(Base):
    __tablename__ = "users"

    user_id         = Column(Integer, primary_key= True, autoincrement= True)
    email           = Column(String(255), nullable= False, unique= True)
    password_hash   = Column(String(255), nullable= False)
    full_name       = Column(String(255), nullable= False)
    role            = Column(Enum("USER", "ADMIN"), default= "USER", nullable= False)
    is_active       = Column(Boolean, default= True, nullable= False)
    created_at      = Column(DateTime, default= datetime.now, nullable= False)

    owned_clubs         = relationship("ClubModel", back_populates= "owner")
    club_memberships    = relationship("ClubMemberModel", back_populates= "user")
    assigned_activities = relationship("ClubActivityModel", back_populates= "assignee")
    club_logs           = relationship("ClubLogModel", back_populates= "actor")
