from fastapi import APIRouter, Depends
from src.presentation.api.dependencies import get_student_command_service, require_role
from src.config import Role
from src.domain.entities.account import Account
from src.application.services.student_command import *
from src.application.dtos.student_command_dto import *
from src.utils import AppError, to_http_exception, HTTPException
import traceback

router = APIRouter(prefix="/students", tags=["Students"], dependencies=[Depends(require_role([Role.ADMIN]))])

# gửi request POST /upload_student với body:
@router.post("/upload", response_model=StudentCommandResponse)
def upload_student(request: CreateStudentRequest,service: StudentCommandManagement = Depends(get_student_command_service)):
    try:
        student_out = service.upload(request)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("❌ ERROR TRACEBACK ❌")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/update", response_model=StudentCommandResponse)
def update_student(request: UpdateStudentRequest,service: StudentCommandManagement = Depends(get_student_command_service)):
    try:
        student_out = service.update(request)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("❌ ERROR TRACEBACK ❌")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{student_id}", response_model=StudentCommandResponse)
def delete_student_endpoint(student_id: str, service: StudentCommandManagement = Depends(get_student_command_service)):
    try:
        # Gọi service để thực hiện nghiệp vụ xóa
        deleted_student = service.delete(student_id)
        return deleted_student
    except ValidationError as e:
        # Lỗi validation từ Service
        raise HTTPException(status_code=400, detail=e.detail)
    except Exception as e:
        # Bắt các lỗi không mong muốn khác
        print("❌ Lỗi không xác định ❌")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi server không xác định: {e}")
