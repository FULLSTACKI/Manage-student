from fastapi import APIRouter, Depends
from src.presentation.api.dependencies import get_student_service
from src.application.services.student import *
from src.application.dtos.student_dto import *
from src.utils import AppError, to_http_exception, HTTPException
import json
from pathlib import Path 

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parents[4]

# gửi request POST /upload_student với body:
@router.post("/student", response_model=UploadStudentResponse)
def upload_student(request: UploadStudentRequest,service: StudentManagement = Depends(get_student_service)):
    try:
        student_out = service.upload(request)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# gửi request POST /get_student với body:
@router.get("/student", response_model=GetStudentResponse)
def get_student_by_id(student_id: str, service: StudentManagement = Depends(get_student_service)):
    try:
        student_out = service.view(student_id)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/student/column")
def get_columns():
    PATH = PROJECT_ROOT / "src/utils/patterns/detail_student.json"
    # 1. Kiểm tra xem file có tồn tại không
    if not PATH.is_file():
        raise HTTPException(status_code=404, detail=f"Configuration file not found.")
    
    try:
        with open(PATH, mode='r',encoding="utf-8") as f:
            data = json.load(f)
        
        # 2. Kiểm tra xem dữ liệu có rỗng không (tùy chọn)
        # Dù list rỗng là hợp lệ, bạn có thể muốn log một cảnh báo
        if not data:
            print(f"Warning: Configuration file at {PATH} is empty.")
        
        return data
        
    except json.JSONDecodeError:
        # 3. Bắt lỗi cụ thể hơn
        raise HTTPException(status_code=500, detail="Error decoding configuration file.")
    except Exception as e:
        # Bắt các lỗi khác
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
@router.get("/student/filter", response_model=StudentFilterOption)
def get_filter_options(columns: str,service: StudentManagement = Depends(get_student_service)):
    try:
        list_col = columns.split(",")
        list_filter_options = service.get_filter_options(list_col)
        return list_filter_options
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))