from src.domain.entities.courses.course import Course
from src.domain.entities.courses.course_repo import IsCourseRepo
from src.models.schemas import UploadCourseRequest, UploadCourseResponse, courseOut
from src.utils.validators import validate_upload_course_request
from src.utils.error.exceptions import ValidationError

class CourseManagement:
    def __init__(self, course_repo: IsCourseRepo):
        self.course_repo = course_repo

    def upload(self, req: UploadCourseRequest) -> UploadCourseResponse:
        err = validate_upload_course_request(req)
        if err:
            raise ValidationError("INVALID_INPUT", detail=err)
        try:
            course_entity = Course.add(
                id=req.id,
                name=req.name,
                credits=req.credits,
                start_course=req.start_course
            )
            
            course_save = self.course_repo.save(course_entity)
        except Exception as e:
            # convert to app-level DB error
            raise ValidationError("DB_ERROR", detail=str(e))
    
        course_out = courseOut.from_entity(course_save)
     
        return UploadCourseResponse(
            success=True,
            message="Course uploaded successfully",
            course=course_out
        )