
from fastapi import FastAPI
from src.infrastructure.persistence.db import Base, engine
from src.data.seed_data import seed_data_if_empty
from .routers import *

app = FastAPI(title="Student Score Management API")


# Tạo bảng khi khởi động (nếu chưa có)
@app.on_event("startup")
def on_startup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_data_if_empty()
    print("✅ Database seeded on startup!")    

for router in list_routers:
    app.include_router(router)