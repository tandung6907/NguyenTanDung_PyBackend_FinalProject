from database.database import Base
from sqlalchemy import Column, Enum, Integer, DateTime, ForeignKey
from datetime import datetime

class ClubMemberModel(Base):
    __tablename__ = "club_members"

    club_id         = Column(Integer, ForeignKey("clubs.club_id"), primary_key= True)
    user_id         = Column(Integer, ForeignKey("users.user_id"), primary_key= True)
    role            = Column(Enum("OWNER", "MEMBER"), nullable= False)
    joined_at       = Column(DateTime, default= datetime.now, nullable= False)