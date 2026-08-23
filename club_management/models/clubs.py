from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class ClubModel(Base):
    __tablename__ = "clubs"

    club_id         = Column(Integer, primary_key= True, autoincrement= True)
    name            = Column(String(255), nullable= False)
    description     = Column(Text, default= None)
    owner_id        = Column(Integer, ForeignKey("users.user_id"), nullable= False)
    created_at      = Column(DateTime, default= datetime.now, nullable= False)
    is_deleted      = Column(Boolean, default= False, nullable= False)
    deleted_at      = Column(DateTime, default= None)

    owner       = relationship("UserModel", back_populates= "owned_clubs")
    members     = relationship("ClubMemberModel", back_populates= "club")
    activities  = relationship("ClubActivityModel", back_populates= "club")
    logs        = relationship("ClubLogModel", back_populates= "club")
