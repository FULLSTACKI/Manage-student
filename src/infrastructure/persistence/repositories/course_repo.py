from sqlalchemy.orm import Session
from src.models.models import Course as CourseModel
from src.domain.entities.courses.course_repo import IsCourseRepo
from src.domain.entities.courses.course import Course
from sqlalchemy.exc import IntegrityError

def _to_model(entity: Course) -> CourseModel:
    return CourseModel(
        id=entity.id,
        name=entity.name,
        credits=entity.credits,
        start_course=entity.start_course,
        end_course=entity.end_course
    )
    
def _to_entity(model: CourseModel) -> Course:
    return Course(
        id=model.id,
        name=model.name,
        credits=model.credits,
        start_course=model.start_course,
        end_course=model.end_course
    )

class CourseRepo(IsCourseRepo):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, course_id: str) -> Course:
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if course:
            return _to_entity(course)
        return None

    def save(self, req_course: Course) -> Course:
        existing = self.get_by_id(req_course.id)
        
        save_course = None 
        
        if existing:
            existing.name = req_course.name
            existing.credits = req_course.credits
            existing.start_course = req_course.start_course 
            existing.end_course = req_course.end_course
            save_course = _to_model(existing)
        else: 
            save_course = _to_model(req_course)
            self.db.add(save_course)
        try:
            self.db.commit()
            self.db.refresh(save_course)
            return _to_entity(save_course)
        except IntegrityError as e:
            errors = str(e)
            self.db.rollback()
            if "UNIQUE constraint failed: course.name" in errors:
                raise ValueError("Name course đã tồn tại.")
            else:
                # Chuyển đổi lỗi kỹ thuật thành lỗi có ý nghĩa hơn cho Application Layer
                raise ValueError(f"Lỗi lưu trữ dữ liệu: {errors}")
        except Exception as e:
            self.db.rollback()
            raise e
        
        