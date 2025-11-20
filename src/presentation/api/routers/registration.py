from fastapi import APIRouter, Depends
from src.presentation.api.dependencies import get_registration_service, require_role
from src.application.services.registration import RegistrationManagement, RegistrationResponse
from src.config import Role
from src.utils import AppError, to_http_exception, HTTPException
import traceback

router = APIRouter(prefix="/students", tags=["Students"], dependencies=[Depends(require_role([Role.STUDENT]))])

@router.post("/register", response_model=RegistrationResponse)
def register(student_id: str, course_id: str,service: RegistrationManagement = Depends(get_registration_service)):
    try:
        registration = service.register(student_id, course_id)
        return registration
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("❌ ERROR TRACEBACK ❌")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))