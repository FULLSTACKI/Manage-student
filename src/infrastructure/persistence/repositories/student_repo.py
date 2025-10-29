from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.repositories import IsStudentRepo
from src.infrastructure.persistence.models import StudentModel, DepartmentModel, CourseModel, RegistrationModel
from src.domain.entities import Student, StudentDetail
from src.infrastructure.persistence.mappers import StudentMapper
from sqlalchemy import select
from typing import List

class StudentRepo(IsStudentRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_by_id(self, student_id:str) -> StudentDetail:
        try:
            stmt = (
                select(
                    StudentModel.student_id,
                    StudentModel.student_name,
                    StudentModel.email,
                    StudentModel.age,
                    StudentModel.birthday,
                    StudentModel.sex,
                    DepartmentModel.department_name
                )
                .select_from(StudentModel)
                .join(DepartmentModel, DepartmentModel.department_id == StudentModel.department_id)
                .filter(StudentModel.student_id == student_id)
            )
            result = self.db_session.execute(stmt).mappings().first()
            return StudentDetail(**result)
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

            return [StudentDetail(
                student_id=data.get("student_id"),
                student_name=data.get("student_name"),
                email=data.get("email"),
                age=data.get("age"),
                birthday=data.get("birthday"),
                sex=data.get("sex"),
                department_name=data.get("department_name"),
                course_name=data.get("course_name")
            ) for data in data_row]
        except Exception as e:
            raise e 
        except IntegrityError as e:
            raise e
    
    def save(self, req_student: Student) -> StudentDetail:
        existing = self.db_session.query(StudentModel).filter(StudentModel.student_id == req_student.student_id).first()
        try:
            if not existing:
                save_student = StudentMapper.to_model(req_student)
                persistent = self.db_session.merge(save_student)
                self.db_session.commit()
                self.db_session.refresh(persistent)
                result = self.get_by_id(req_student.student_id)
                return result 
        except IntegrityError as e:
            self.db_session.rollback()
            raise e
        except Exception as e:
            self.db_session.rollback()
            raise e 
    
    def update(self, req: Student) -> StudentDetail:
        existing = self.db_session.query(StudentModel).filter(StudentModel.student_id == req.student_id).first()
        try:
            if existing:
                existing.student_name = req.student_name
                existing.email = req.email
                existing.birthday = req.birthday 
                existing.age = req.age
                existing.sex = req.sex 
                existing.department_id = req.department_id
                update_student = existing
            persistent = self.db_session.merge(update_student)
            self.db_session.commit()
            self.db_session.refresh(persistent)
            result = self.get_by_id(req.student_id)
            return result
        except IntegrityError as e:
            self.db_session.rollback()
            raise e
        except Exception as e:
            self.db_session.rollback()
            raise e 

    def deleted(self, student_id: str) -> StudentDetail:
        try:
            stmt = (
                select(
                    StudentModel,
                    DepartmentModel.department_name
                )
                .select_from(StudentModel)
                .join(DepartmentModel, DepartmentModel.department_id == StudentModel.department_id)
                .filter(StudentModel.student_id == student_id)
            )
            result_row = self.db_session.execute(stmt).first()
            student_model_to_delete = result_row[0]
            department_name = result_row[1]
            deleted_student_detail = StudentDetail(
                student_id=student_model_to_delete.student_id,
                student_name=student_model_to_delete.student_name,
                email=student_model_to_delete.email,
                age=student_model_to_delete.age,
                birthday=student_model_to_delete.birthday,
                sex=student_model_to_delete.sex,
                department_name=department_name
            )
            self.db_session.delete(student_model_to_delete)
            self.db_session.commit()
            return deleted_student_detail
        except IntegrityError as e: 
            self.db_session.rollback()
            raise e
        except Exception as e:
            self.db_session.rollback()
            raise e