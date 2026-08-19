from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from datetime import datetime

class ClubModel(Base):
    __tablename__ = "clubs"

    club_id         = Column(Integer, primary_key= True, autoincrement= True)
    name            = Column(String(255), nullable= False)
    description     = Column(Text, default= None)
    owner_id        = Column(Integer, ForeignKey("users.user_id"), nullable= False)
    created_at      = Column(DateTime, default= datetime.now, nullable= False)
