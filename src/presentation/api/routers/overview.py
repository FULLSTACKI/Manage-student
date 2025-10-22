from fastapi import APIRouter, Depends
from src.application.services.overview import *
from src.application.dtos.overview_dto import *
from src.presentation.api.dependencies import get_overview_service
from src.utils import  HTTPException, AppError, to_http_exception

router = APIRouter()

# gửi request GET /important_kpi với body:
@router.get("/overview", response_model=OverviewResponse)
def get_overview(service: OverviewManagement = Depends(get_overview_service)):
    try:
        kpi, top3 = service.view_detail_all()
        return {"kpi": kpi, "top3_student": top3}
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        # Bắt các lỗi khác
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
