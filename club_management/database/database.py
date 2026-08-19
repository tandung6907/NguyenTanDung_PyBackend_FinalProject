from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.setting import DB_URL

engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush= False, autocommit= False, bind= engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
