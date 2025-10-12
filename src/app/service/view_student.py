from src.infrastructure.repo.student_repo import StudentRepo
from src.utils.validators import validate_id
from src.utils.error.error_handling import to_http_exception
from src.utils.error.exceptions import ValidationError
from src.models.schemas import GetStudentRequest, studentOut, GetStudentResponse

class ViewStudent:
    def __init__(self, db_session=None):
        self.student_repo = StudentRepo(db_session=db_session)

    def view(self, req: GetStudentRequest) -> GetStudentResponse:
        if not validate_id(req.id) or not self.student_repo.exist(req.id):
            raise ValidationError("INVALID_INPUT", detail="student_id is invalid")
        
        # ensure student exists
        student = self.student_repo.get(req.id)
        
        if not student:
            raise ValidationError("NOT_FOUND", detail=f"student {req.id} not found")
        
        return GetStudentResponse(
            success=True,
            message="Student retrieved successfully",
            student=student_out
        )   