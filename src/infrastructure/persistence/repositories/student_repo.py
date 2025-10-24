from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.repositories import IsStudentRepo
from src.infrastructure.persistence.models import StudentModel
from src.domain.entities import Student
from typing import List

def _to_model(entity: Student) -> StudentModel:
    return StudentModel(
        student_id=entity.student_id,
        student_name=entity.student_name,
        email=entity.email,
        birthday=entity.birthday,
        age=entity.age,
        sex=entity.sex,
        department_id = entity.department_id
    )
    
def _to_entity(model: StudentModel) -> Student:
    return Student(
        student_id=model.student_id,
        student_name=model.student_name,
        email=model.email,
        birthday=model.birthday,
        age=model.age,
        sex=model.sex,
        department_id=model.department_id
    )

class StudentRepo(IsStudentRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_by_id(self, student_id:str) -> Student:
        db_model = self.db_session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        if db_model:
            return _to_entity(db_model)
        return None
    
    
    def save(self, req_student: Student) -> Student:
        existing = self.get_by_id(req_student.student_id)
        
        save_student = None 
        
        if existing:
            existing.student_name = req_student.student_name
            existing.email = req_student.email
            existing.age = req_student.age 
            existing.birthday = req_student.birthday
            existing.sex = req_student.sex
            existing.department_id = req_student.department_id
            save_student = _to_model(existing)
        else: 
            save_student = _to_model(req_student)
        try:
            persistent = self.db_session.merge(save_student)
            self.db_session.commit()
            self.db_session.refresh(persistent)
            return _to_entity(persistent)
        except IntegrityError as e:
            errors = str(e)
            self.db_session.rollback()
            if "UNIQUE constraint failed: students.email" in errors:
                raise ValueError("Email đã tồn tại. Vui lòng sử dụng một địa chỉ email khác.")
            else:
                # Chuyển đổi lỗi kỹ thuật thành lỗi có ý nghĩa hơn cho Application Layer
                raise ValueError(f"Lỗi lưu trữ dữ liệu: {errors}")
        except Exception as e:
            self.db_session.rollback()
            raise e
        