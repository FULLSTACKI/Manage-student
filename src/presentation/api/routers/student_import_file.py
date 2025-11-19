from fastapi import APIRouter, Depends, UploadFile
from src.presentation.api.dependencies import get_student_import_file_service, require_role
from src.config import Role
from src.application.services.student_import_file import *
from src.application.dtos.student_command_dto import *
from src.utils import AppError, to_http_exception, HTTPException
import traceback

router = APIRouter(prefix="/students", tags=["Students"], dependencies=[Depends(require_role([Role.ADMIN]))])

@router.post("/import_file", response_model=StudentCommandResponse)
async def import_students_from_docx(files: List[UploadFile], service: StudentImportFileManagement = Depends(get_student_import_file_service)):
    try:
        saved_entities = await service.import_students_from_docx(files=files)
        return saved_entities
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        # Bắt các lỗi không mong muốn khác
        print("❌ Lỗi không xác định ❌")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi server không xác định: {e}")