
from fastapi import FastAPI
from src.infrastructure.persistence.db import Base, engine
from src.data.seed_data import seed_data_if_empty
from .routers import *
from src.data.backups_data import _do_backup
from src.data.clean_backup import cleanup_by_file_count

app = FastAPI(title="Student Score Management API")


# Tạo bảng khi khởi động (nếu chưa có)
@app.on_event("startup")
def on_startup():
    print("🚀 Starting application...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_data_if_empty()
    _do_backup()
    cleanup_by_file_count()
    print("✅ Database initialized and backup created.")
    
@app.on_event("shutdown")
def on_shutdown():
    _do_backup()
    print("👋 Application shutting down, final backup done!")
    

for router in list_routers:
    app.include_router(router)