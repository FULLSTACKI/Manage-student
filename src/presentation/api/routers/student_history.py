from fastapi import APIRouter, Depends
from ..dependencies import get_student_history_service, require_role
from src.config import Role
from src.domain.entities.account import Account
from src.application.services.student_history import StudentHistoryManagement
from src.application.dtos.student_history_dto import StudentHistoryResp
from src.utils import AppError, to_http_exception, HTTPException
from typing import List
import traceback

router = APIRouter(prefix="/students", tags=["Students"], dependencies=[Depends(require_role([Role.ADMIN]))])

@router.get("/history", response_model=List[StudentHistoryResp])
def get_list_student_history(service: StudentHistoryManagement = Depends(get_student_history_service)):
    try:
        list_student = service.get_list_student_history()
        return list_student
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("❌ ERROR TRACEBACK ❌")
        traceback.print_exc()   # 👉 in toàn bộ lỗi ra terminal
        raise HTTPException(status_code=500, detail=str(e))