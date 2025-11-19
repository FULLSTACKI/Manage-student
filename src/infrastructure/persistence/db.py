from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import DB_URL

# Kết nối cơ sở dữ liệu SQLite (có thể thay đổi sang MySQL/PostgreSQL nếu cần)
try:
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

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
