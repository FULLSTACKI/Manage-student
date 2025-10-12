from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Kết nối cơ sở dữ liệu SQLite (có thể thay đổi sang MySQL/PostgreSQL nếu cần)
DATABASE_URL = "sqlite:///./student_score.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
