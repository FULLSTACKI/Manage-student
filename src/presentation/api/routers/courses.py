from fastapi import APIRouter, Depends
from ..dependencies import get_course_service
from src.application.services.course import *
from src.application.dtos.course_dto import *
from src.utils import AppError, to_http_exception, HTTPException

router = APIRouter()
# gửi request POST /upload_course với body:
@router.post("/courses", response_model=UploadCourseResponse)
def upload_course(request: UploadCourseRequest, service: CourseManagement = Depends(get_course_service)):
    try:
        course_out = service.upload(request)
        return course_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# gửi request POST /get_course với body:
@router.get("/courses/{course_id}", response_model=GetCourseResponse)
def get_course(course_id:str, service: CourseManagement = Depends(get_course_service)):
    try:
        course_out = service.view(course_id)
        return course_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))