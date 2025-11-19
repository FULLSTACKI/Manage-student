from fastapi import APIRouter, Depends
from src.presentation.api.dependencies import require_role
from src.config import DETAIL_STUDENT_CONFIG, ANALYTIC_CONFIG, Role
from src.utils import HTTPException

router = APIRouter(dependencies=[Depends(require_role([Role.ADMIN]))])

@router.get("/students/column")
def get_columns():
    if not DETAIL_STUDENT_CONFIG:
        raise HTTPException(status_code=404, detail="Config file 'detail_student.json' not found.")
    return DETAIL_STUDENT_CONFIG

@router.get("/overview/table_analytic")
def get_analytics_view():    
    if not ANALYTIC_CONFIG:
        raise HTTPException(status_code=404, detail="Config file 'analytic.json' not found.")
    return ANALYTIC_CONFIG