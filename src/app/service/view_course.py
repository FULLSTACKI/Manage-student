from src.repo.course_repo import CourseRepo
from src.utils.validators import validate_id
from src.utils.error.error_handling import to_http_exception
from src.utils.error.exceptions import ValidationError
from src.models.schemas import GetCourseRequest, GetCourseResponse, courseOut

class ViewCourse:
    def __init__(self, db_session=None):
        self.course_repo = CourseRepo(db_session = db_session)

    def view(self, req: GetCourseRequest) -> GetCourseResponse:
        if not validate_id(req.id) or not self.course_repo.exist(req.id):
            raise ValidationError("INVALID_INPUT", detail="course_id is invalid")
        
        # ensure course exists
        course = self.course_repo.get(req.id)
        
        if not course:
            raise ValidationError("NOT_FOUND", detail=f"course {req.id} not found")
        
        course_out = courseOut(
            id=course.id,
            name=course.name,
            credits=course.credits,
            start_course=course.start_course,
            end_course=course.end_course
        )
        return GetCourseResponse(
            success=True,
            message="Course retrieved successfully",
            course=course_out
        )   