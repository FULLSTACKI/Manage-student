from fastapi import APIRouter, Depends
from src.presentation.api.dependencies import get_student_service
from src.application.services.student import *
from src.application.dtos.student_dto import *
from src.utils import AppError, to_http_exception, HTTPException
import json
from pathlib import Path 

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
path = "src/utils/patterns"

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
    
@router.get("/students/columns", response_model=StudentQueryByColumns)
def get_columns():
    PATH = PROJECT_ROOT / "src/utils/patterns/detail_student.json"
    print(f"DEBUG: Server is trying to read file from this absolute path: {PATH.resolve()}")
    # 1. Kiểm tra xem file có tồn tại không
    if not PATH.is_file():
        raise HTTPException(status_code=404, detail=f"Configuration file not found.")
    try:
        with open(PATH, mode='r', encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/students/filters", response_model=StudentFilterOption)
def get_filter_options(columns: List[str],service: StudentManagement = Depends(get_student_service)):
    try:
        list_filter_options = service.get_filter_options(columns)
        return list_filter_options
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# if __name__ == "__main__":
#    data = get_columns()
#    print(data)