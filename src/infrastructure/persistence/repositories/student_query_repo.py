from src.infrastructure.persistence.models import StudentModel, CourseModel, DepartmentModel, RegistrationModel
from src.application.dtos import studentOut
from src.domain.repositories import IsStudentQueryRepo
from src.infrastructure.persistence.mappers import StudentQueryMapper
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

class StudentQueryRepo(IsStudentQueryRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_list_detail_student(self, col: List[str], department_id:List[str] = None, course_id:List[str] = None):
            try: 
                columns = StudentQueryMapper.map_col(col)

                stmt = (
                    select(*columns)
                    .select_from(StudentModel)
                    .join(DepartmentModel)
                    .join(RegistrationModel)
                    .join(CourseModel)
                    .group_by(StudentModel.student_id, *columns)
                )
                
                if "departments" in col and department_id:
                    stmt = stmt.where(StudentModel.department_id.in_(department_id))
                if "courses" in col and course_id:
                    stmt = stmt.where(RegistrationModel.course_id.in_(course_id))

                data_row = self.db_session.execute(stmt).mappings().all()
                return [studentOut(**data) for data in data_row]
            except Exception as e:
                raise e 
            except IntegrityError as e:
                raise e
    
    def get_by_id(self, student_id:str) -> studentOut:
        try:
            result = self.db_session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
            return StudentQueryMapper.to_detail(result)
        except IntegrityError as e: 
            raise e
        except Exception as e:
            raise e