from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.repositories import IsStudentRepo
from src.infrastructure.persistence.models import Student as StudentModel
from src.domain.entities import Student

def _to_model(entity: Student) -> StudentModel:
    return StudentModel(
        id=entity.id,
        name=entity.name,
        email=entity.email,
        birthday=entity.birthday,
        age=entity.age,
        sex=entity.sex
    )
    
def _to_entity(model: StudentModel) -> Student:
    return Student(
        id=model.id,
        name=model.name,
        email=model.email,
        birthday=model.birthday,
        age=model.age,
        sex=model.sex
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
        existing = self.get_by_id(req_student.id)
        
        save_student = None 
        
        if existing:
            existing.name = req_student.name
            existing.email = req_student.email
            existing.age = req_student.age 
            existing.birthday = req_student.birthday
            existing.sex = req_student.sex
            save_student = _to_model(existing)
        else: 
            save_student = _to_model(req_student)
            self.db_session.add(save_student)
        try:
            self.db_session.commit()
            self.db_session.refresh(save_student)
            return _to_entity(save_student)
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
        