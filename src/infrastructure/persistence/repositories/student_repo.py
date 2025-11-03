from src.infrastructure.persistence.models import StudentModel, CourseModel, DepartmentModel, RegistrationModel
from src.domain.entities import Student
from src.application.dtos import studentOut
from src.domain.repositories import IsStudentRepo
from src.infrastructure.persistence.mappers import StudentMapper
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

class StudentRepo(IsStudentRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_by_id(self, student_id:str) -> studentOut:
        try:
            result = self.db_session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
            return StudentMapper.to_detail(result)
        except IntegrityError as e: 
            raise e
        except Exception as e:
            raise e
    
    def get_list_detail_student(self, col: List[str], department_id:List[str] = None, course_id:List[str] = None):
        try: 
            columns = StudentMapper.map_col(col)

            stmt = (
                select(*columns)
                .select_from(StudentModel)
                .join(DepartmentModel)
                .join(RegistrationModel)
                .join(CourseModel)
            )
            
            if "departments" in col and department_id:
                stmt = stmt.where(StudentModel.department_id.in_(department_id))
            if "courses" in col and course_id:
                stmt = stmt.where(RegistrationModel.course_id.in_(course_id))

            data_row = self.db_session.execute(stmt).mappings().all()

            return [studentOut(
                student_id=data.get("student_id"),
                student_name=data.get("student_name"),
                email=data.get("email"),
                age=f"{data.get("age")}",
                birthday=f"{data.get("birthday")}",
                sex=data.get("sex"),
                departments=data.get("department_name"),
                courses=data.get("course_name"),
                birthplace=data.get("birthplace"),
                address=data.get("address"),
                phone=data.get("phone"),
                ethnicity=data.get("ethnicity"),
                religion=data.get("religion"),
                id_card=data.get("id_card"),
                issue_date=f"{data.get("issue_date")}",
                issue_place=data.get("issue_place")
            ) for data in data_row]
        except Exception as e:
            raise e 
        except IntegrityError as e:
            raise e
    
    def save(self, req_student: Student) -> studentOut:
        existing = self.db_session.query(StudentModel).filter(StudentModel.student_id == req_student.student_id).first()
        try:
            if not existing:
                save_student = StudentMapper.to_model(req_student)
                persistent = self.db_session.merge(save_student)
                self.db_session.commit()
                self.db_session.refresh(persistent)
                _ = persistent.department
                return StudentMapper.to_detail(persistent)
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
    
    def update(self, req: Student) -> studentOut:
        existing = self.db_session.query(StudentModel).filter(StudentModel.student_id == req.student_id).first()
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
            return StudentMapper.to_detail(existing)
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

    def deleted(self, student_id: str) -> studentOut:
        try:
            result = self.db_session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
            deleted_student_detail = StudentMapper.to_detail(result)
            self.db_session.delete(result)
            self.db_session.commit()
            return deleted_student_detail
        except IntegrityError as e: 
            self.db_session.rollback()
            raise e
        except Exception as e:
            self.db_session.rollback()
            raise e
