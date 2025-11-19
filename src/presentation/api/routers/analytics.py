from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from src.config import Role
from src.application.services.analytic import *
from src.application.dtos import *
from src.presentation.api.dependencies import get_analytic_service, require_role
from src.utils import  HTTPException, AppError, to_http_exception
import traceback

router = APIRouter(prefix="/overview",tags=["Overview"],dependencies=[Depends(require_role([Role.ADMIN]))])

@router.post("/analytic", response_model=list[dict])
def analytic(req: AnalyticsRequest, service: AnalyticManagement = Depends(get_analytic_service)):
    try:
        query_out = service.get_analytic(req.dimension, req.metric, req.agg)
        return query_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("Bắt ngoại lỗi tại:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export", response_model=None)
async def export(req: ReportDTO, service: AnalyticManagement = Depends(get_analytic_service)):
    try:
        file_bytes_io, content_type, filename = await service.export_file(req)
        
        # 2. Định nghĩa Headers để trình duyệt biết đây là file tải về
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }

        # 3. Trả về StreamingResponse
        # Nó sẽ truyền trực tiếp file_bytes_io về cho client
        return StreamingResponse(
            file_bytes_io, 
            media_type=content_type, 
            headers=headers
        )
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        print("Bắt ngoại lỗi tại:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))