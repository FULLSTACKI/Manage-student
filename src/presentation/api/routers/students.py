from fastapi import APIRouter, Depends
from ..dependencies import get_student_service
from src.application.services.student import *
from src.application.dtos.student_dto import *
from src.utils import AppError, to_http_exception, HTTPException

router = APIRouter()

# gửi request POST /upload_student với body:
@router.post("/students", response_model=UploadStudentResponse)
def upload_student(request: UploadStudentRequest,service: StudentManagement = Depends(get_student_service)):
    try:
        student_out = service.upload(request)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# gửi request POST /get_student với body:
@router.get("/students/{student_id}", response_model=GetStudentResponse)
def get_student_by_id(student_id: str, service: StudentManagement = Depends(get_student_service)):
    try:
        student_out = service.view(student_id)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/students", response_model=List[studentOut])
def get_all_student(service: StudentManagement = Depends(get_student_service)):
    try:
        list_student_out = service.get_all()
        return list_student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))