from src.domain.entities import Course
from src.domain.repositories import IsCourseRepo
from src.application.dtos.course_dto import *
from src.utils import validate_id, ValidationError

class CourseManagement:
    def __init__(self, course_repo: IsCourseRepo):
        self.course_repo = course_repo

    def upload(self, req: UploadCourseRequest) -> UploadCourseResponse:
        # err = validate_upload_course_request(req)
        # if err:
        #     raise ValidationError("INVALID_INPUT", detail=err)
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
        
    def get_by_id(self, course_id: str) -> Course:
        if not validate_id(course_id):
            raise ValidationError("INVALID_INPUT", detail="course_id format is invalid")
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValidationError("NOT_FOUND",detail=f"course {course_id} not found")
        return course

    def view(self, course_id:str) -> GetCourseResponse:
        course_entity = self.get_by_id(course_id)
        course_out = courseOut.from_entity(course_entity)
        return GetCourseResponse(
            success=True,
            message="Course retrieved successfully",
            course=course_out
        )