from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db, Base, engine
from src.database.seed_data import seed_data_if_empty
from src.models.schemas import (
    UploadScoreRequest,
    UploadScoreResponse,
    # GetScoreRequest,
    # GetScoreResponse,
    UploadStudentRequest,
    UploadStudentResponse,
    # GetStudentRequest,
    # GetStudentResponse,
    UploadCourseRequest,
    UploadCourseResponse,
    # GetCourseRequest,
    # GetCourseResponse,
)
from src.app.service.course import CourseManagement
# from src.service.view_course import ViewCourse
from src.app.service.score import ScoreManagement
# from src.service.view_score import ViewScore
from src.app.service.student import StudentManagement
# from src.service.view_student import ViewStudent
from src.utils.error.error_handling import to_http_exception
from src.utils.error.exceptions import AppError
from src.app.api.dependencies import get_student_service, get_course_service, get_score_service

app = FastAPI(title="Student Score Management API")


# Tạo bảng khi khởi động (nếu chưa có)
@app.on_event("startup")
def on_startup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_data_if_empty()
    print("✅ Database seeded on startup!")    
    
# gửi request POST /upload_score với body:
@app.post("/upload_score", response_model=UploadScoreResponse)
def upload_score(request: UploadScoreRequest, service:ScoreManagement = Depends(get_score_service)):
    try:
        result = service.upload(request)
        return result
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# # gửi request POST /get_score với body:
# @app.post("/get_score", response_model=GetScoreResponse)
# def get_score(request: GetScoreRequest, db: Session = Depends(get_db)):
#     service = ViewScore(db_session=db)
#     try:
#         score_out = service.view(request)
#         return score_out
#     except AppError as e:
#         raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# gửi request POST /upload_student với body:
@app.post("/upload_student", response_model=UploadStudentResponse)
def upload_student(request: UploadStudentRequest,service: StudentManagement = Depends(get_student_service)):
    try:
        student_out = service.upload(request)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# # gửi request POST /get_student với body:
# @app.post("/get_student", response_model=GetStudentResponse)
# def get_student(request: GetStudentRequest, db: Session = Depends(get_db)):
#     service = ViewStudent(db_session=db)
#     try:
#         student_out = service.view(request)
#         return student_out
#     except AppError as e:
#         raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# gửi request POST /upload_course với body:
@app.post("/upload_course", response_model=UploadCourseResponse)
def upload_course(request: UploadCourseRequest, service: CourseManagement = Depends(get_course_service)):
    try:
        course_out = service.upload(request)
        return course_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# # gửi request POST /get_course với body:
# @app.post("/get_course", response_model=GetCourseResponse)
# def get_course(request: GetCourseRequest, db: Session = Depends(get_db)):
#     service = ViewCourse(db_session=db)
#     try:
#         course_out = service.view(request)
#         return course_out
#     except AppError as e:
#         raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))