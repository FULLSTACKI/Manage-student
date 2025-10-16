from fastapi import APIRouter, Depends
from ..dependencies import get_score_service
from src.application.services.score import *
from src.application.dtos.score_dto import *
from src.utils import AppError, to_http_exception, HTTPException

router = APIRouter()
# gửi request POST /upload_score với body:
@router.post("/Scores", response_model=UploadScoreResponse)
def upload_score(request: UploadScoreRequest, service:ScoreManagement = Depends(get_score_service)):
    try:
        result = service.upload(request)
        return result
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# gửi request POST /get_score với body:
@router.get("/students/{student_id}/courses/{course_id}/Scores", response_model=GetScoreResponse)
def get_score(student_id: str, course_id: str, service: ScoreManagement = Depends(get_score_service)):
    try:
        score_out = service.view(student_id,course_id)
        return score_out
    except AppError as e:
        raise to_http_exception(getattr(e, "code", "INTERNAL_ERROR"), str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))