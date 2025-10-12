from src.utils.validators import validate_upload_score_request
from src.utils.error.exceptions import ValidationError
from src.models.schemas import UploadScoreResponse, UploadScoreRequest, ScoreOut
from src.domain.entities.scores.score import Score
from src.domain.entities.registrations.registration_repo import IsRegistrationRepo
from src.domain.entities.scores.score_repo import IsScoreRepo

class ScoreManagement:
    def __init__(self, score_repo: IsScoreRepo, regis_repo: IsRegistrationRepo):
        self.score_repo = score_repo 
        self.regis_repo = regis_repo

    def upload(self, req: UploadScoreRequest) -> UploadScoreResponse:
        err = validate_upload_score_request(req)
        if err:
            # raise app-level ValidationError which caller/controller can map
            raise ValidationError("INVALID_INPUT", detail=err)
        
        if not self.regis_repo.get_by_id(req.student_id, req.course_id):
            raise ValidationError("ALREADY_REGISTERED", detail= f"Sinh viên {req.student_id} hoặc môn học {req.course_id} không tồn tại!")
        
        try:
            score_entity = Score.add(
                student_id=req.student_id,
                course_id=req.course_id,
                coursework_grade=req.coursework_grade,
                midterm_grade=req.midterm_grade,
                final_grade=req.final_grade
            )
            score_save = self.score_repo.save(score_entity)
        except Exception as e:
            raise ValidationError("DB_ERROR", detail=str(e))
        
        score_out = ScoreOut.from_entity(score_save)
        
        return UploadScoreResponse(
            success=True,
            message="Saved",
            score=score_out
        )
