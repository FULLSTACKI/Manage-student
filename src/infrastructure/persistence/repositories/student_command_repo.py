from src.infrastructure.persistence.models import StudentModel
from src.domain.entities import Student
from src.domain.repositories import IsStudentCommandRepo
from src.infrastructure.persistence.mappers import StudentCommandMapper
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class StudentCommandRepo(IsStudentCommandRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def find_by_id(self, student_id:str) -> StudentModel:
        try:
            result = self.db_session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
            return result
        except IntegrityError as e: 
            raise e
        except Exception as e:
            raise e
    
    def save(self, req_student: Student) -> Student:
        existing = self.find_by_id(req_student.student_id)
        try:
            if not existing:
                save_student = StudentCommandMapper.to_model(req_student)
                persistent = self.db_session.merge(save_student)
                self.db_session.commit()
                self.db_session.refresh(persistent)
                return req_student
        except IntegrityError as e:
            self.db_session.rollback()
            error_info = str(e.orig)
            if "UNIQUE constraint failed: students.id_card" in error_info:
                raise ValueError(f"CCCD đã tồn tại: {req_student.id_card}")
            else:
                raise e
        except Exception as e:
            self.db_session.rollback()
            raise e 
    
    def update(self, req: Student) -> Student:
        existing = self.find_by_id(req.student_id)
        try:
            if existing:
                existing.student_name = req.student_name
                existing.email = req.email
                existing.birthday = req.birthday 
                existing.age = req.age
                existing.sex = req.sex 
                existing.department_id = req.department_id
                existing.birthplace = req.birthplace
                existing.address = req.address
                existing.phone = req.phone
                existing.ethnicity = req.ethnicity
                existing.religion = req.religion
                existing.id_card = req.id_card
                existing.issue_date = req.issue_date
                existing.issue_place = req.issue_place
            self.db_session.commit()
            self.db_session.refresh(existing)
            return req
        except IntegrityError as e:
            self.db_session.rollback()
            error_info = str(e.orig)
            if "UNIQUE constraint failed: students.id_card" in error_info:
                raise ValueError(f"CCCD đã tồn tại: {req.id_card}")
            else:
                raise e
        except Exception as e:
            self.db_session.rollback()
            raise e 

    def deleted(self, student_id: str) -> Student:
        try:
            result = self.find_by_id(student_id)
            self.db_session.delete(result)
            self.db_session.commit()
            return student_id
        except IntegrityError as e: 
            self.db_session.rollback()
            raise e
        except Exception as e:
            self.db_session.rollback()
            raise e
