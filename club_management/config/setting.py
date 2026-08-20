import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", SECRET_KEY)
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", "7"))