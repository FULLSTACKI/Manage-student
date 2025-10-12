from src.repo.student_repo import StudentRepo
from src.repo.course_repo import CourseRepo
from src.repo.score_repo import ScoreRepo
from src.repo.registration_repo import RegistrationRepo
from src.utils.validators import validate_id
from src.utils.error.error_handling import to_http_exception
from src.utils.error.exceptions import ValidationError
from src.models.schemas import GetScoreRequest, ScoreOut, GetScoreResponse

class ViewScore:
    def __init__(self, db_session=None):
        self.student_repo = StudentRepo(db_session=db_session)
        self.course_repo = CourseRepo(db_session=db_session)
        self.score_repo = ScoreRepo(db_session=db_session)
        self.registration_repo = RegistrationRepo(db_session=db_session)

    def view(self, req: GetScoreRequest) -> GetScoreResponse:
        # ensure student exists
        if not self.student_repo.exist(req.student_id) or not validate_id(req.student_id):
            raise ValidationError("NOT_FOUND", detail=f"student {req.student_id} not found")

        # ensure course exists
        if not self.course_repo.exist(req.course_id) or not validate_id(req.course_id):
            raise ValidationError("NOT_FOUND", detail=f"course {req.course_id} not found")
        
        # ensure student is registered for the course
        if not self.registration_repo.exist(req.student_id, req.course_id):
            raise ValidationError("ALREADY_REGISTERED", detail=f"student {req.student_id} is not registered for course {req.course_id}")
        
        # fetch score
        score = self.score_repo.get(req.student_id, req.course_id)
        if not score:
            raise ValidationError("NOT_FOUND", detail=f"score for student {req.student_id} in course {req.course_id} not found")
        
        score_out = ScoreOut(
            student_id=score.student_id,
            course_id=score.course_id,
            coursework_grade=score.coursework_grade,
            midterm_grade=score.midterm_grade,
            final_grade=score.final_grade,
            gpa=score.gpa,
        )
        return GetScoreResponse(
            success=True,   
            message="Score retrieved successfully",
            score=score_out
        )