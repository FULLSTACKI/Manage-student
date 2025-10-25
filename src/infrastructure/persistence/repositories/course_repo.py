from sqlalchemy.orm import Session
from src.infrastructure.persistence.models import CourseModel
from src.domain.repositories.course_repo import IsCourseRepo
from src.domain.entities import Course, Option
from sqlalchemy.exc import IntegrityError
from typing import List
from sqlalchemy import text

class CourseRepo(IsCourseRepo):
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def get_filter_all(self) -> List[Course]:
        try:
            query = text("SELECT course_id, course_name FROM courses")
            result = self.db.execute(query)
            course_row = result.mappings().all()
            list_course = [Option(id=data.course_id,name=data.course_name) for data in course_row]
            return list_course
        except Exception as e:
            raise  e
        
    def get_by_id(self, course_id: str) -> Course:
        course = self.db.query(CourseModel).filter(CourseModel.course_id == course_id).first()
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
            existing.department_id = req_course.department_id
            save_course = _to_model(existing)
        else: 
            save_course = _to_model(req_course)
        try:
            persistent = self.db.merge(save_course)
            self.db.commit()
            self.db.refresh(persistent)
            return _to_entity(persistent)
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
        
        