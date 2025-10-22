from fastapi import APIRouter, Depends
from src.application.services.analytic import *
from src.application.dtos.analytic_view_dto import *
from src.presentation.api.dependencies import get_analytic_department_service
from src.utils import  HTTPException, AppError, to_http_exception
from pathlib import Path
import json

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
# gửi request GET /analytics_view với body:
@router.get("/analytics_view", response_model=List[AnalyticsViewDTO])
def get_analytics_view():
    # Xây dựng đường dẫn từ thư mục gốc, dễ đọc và an toàn hơn
    PATH = PROJECT_ROOT / "src/utils/patterns/analytic.json"
    
    # THÊM DÒNG NÀY ĐỂ DEBUG
    print(f"DEBUG: Server is trying to read file from this absolute path: {PATH.resolve()}")
    # 1. Kiểm tra xem file có tồn tại không
    if not PATH.is_file():
        raise HTTPException(status_code=404, detail=f"Configuration file not found.")
    
    try:
        with open(PATH, mode='r', encoding="utf-8") as f:
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
    
@router.post("/analytic_post", response_model=List[AnalyticsResponse])
def upload_analytic_department(req: AnalyticsRequest, service: AnalyticManagement = Depends(get_analytic_department_service)):
    try:
        query_out = service.get_analytic_department_view(req)
        return query_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))