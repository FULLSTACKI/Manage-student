from fastapi import APIRouter, Depends
from src.presentation.api.dependencies import get_student_query_service, require_role
from src.domain.entities.account import Account
from src.config import Role
from src.application.services import *
from src.application.dtos.student_query_dto import *
from src.utils import AppError, to_http_exception, HTTPException
import traceback

router = APIRouter(prefix="/students", tags=["Students"])

# gửi request POST /get_student với body:
@router.get("", response_model=StudentResponse, dependencies=[Depends(require_role([Role.ADMIN, Role.STUDENT]))]) 
def get_student_by_id(student_id: str, service: StudentQueryManagement = Depends(get_student_query_service)):
    try:    
        student_out = service.get_by_id(student_id)
        return student_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/filter", response_model=StudentFilterOption, dependencies=[Depends(require_role([Role.ADMIN]))]) 
def get_filter_options(columns: str,service: StudentQueryManagement = Depends(get_student_query_service)):
    try:
        list_col = columns.split(",")
        list_filter_options = service.get_filter_options(list_col)
        return list_filter_options
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/list", response_model=List[studentOut], dependencies=[Depends(require_role([Role.ADMIN]))])  
def get_list_student(req: StudentDetailRequest,service: StudentQueryManagement = Depends(get_student_query_service)):
    try:
        list_student = service.get_detail_students(req)
        return list_student
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("❌ ERROR TRACEBACK ❌")
        traceback.print_exc()   # 👉 in toàn bộ lỗi ra terminal
        raise HTTPException(status_code=500, detail=str(e))