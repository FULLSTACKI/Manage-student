from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Kết nối cơ sở dữ liệu SQLite (có thể thay đổi sang MySQL/PostgreSQL nếu cần)
DATABASE = os.getenv("DATABASE_URL")
try:
    engine = create_engine(DATABASE, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
