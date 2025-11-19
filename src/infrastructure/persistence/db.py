from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import DB_URL

# Kết nối cơ sở dữ liệu SQLite (có thể thay đổi sang MySQL/PostgreSQL nếu cần)
try:
    db_url = DB_URL

    # Fix lỗi 1: SQLAlchemy đời mới bắt buộc dùng postgresql:// thay vì postgres:// (Render hay trả về postgres://)
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # Fix lỗi 2: Chỉ dùng check_same_thread nếu là SQLite
    connect_args = {}
    if "sqlite" in db_url:
        connect_args = {"check_same_thread": False}

    # Tạo engine với tham số động
    engine = create_engine(
        db_url,
        connect_args=connect_args, # Postgres sẽ nhận dict rỗng {}, SQLite nhận dict có check_same_thread
        pool_pre_ping=True # Nên thêm cái này để giữ kết nối ổn định
    )

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
