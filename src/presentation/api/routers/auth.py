from fastapi import APIRouter, Depends
from src.application.services import AccountManagement
from src.application.dtos.account_dto import *
from src.presentation.api.dependencies import get_account_service
from src.utils import AppError, to_http_exception, HTTPException
import traceback

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=AccountResponse)
def login(req: AccountLoginRequest, service: AccountManagement = Depends(get_account_service)):
    try:
        account = service.login(req)
        return account
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("❌ ERROR TRACEBACK ❌")
        traceback.print_exc()   # 👉 in toàn bộ lỗi ra terminal
        raise HTTPException(status_code=500, detail=str(e))
