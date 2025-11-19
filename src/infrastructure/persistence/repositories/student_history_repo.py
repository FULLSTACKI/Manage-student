from src.domain.repositories import IsStudentHistoryRepo
from src.infrastructure.persistence.models import StudentHistoryModel, DepartmentModel
from src.application.dtos import StudentHistoryResp
from ..mappers import StudentHistoryMapper
from sqlalchemy import select
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class StudentHistoryRepo(IsStudentHistoryRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_list_student_history(self) -> List[StudentHistoryResp]:
        try: 
            query = (
                select(
                    StudentHistoryModel,
                    DepartmentModel.department_name
                ).select_from(StudentHistoryModel)
                .join(DepartmentModel, DepartmentModel.department_id == StudentHistoryModel.department_id)
                .order_by(StudentHistoryModel.changed_at.desc())
            )
            data_row = self.db_session.execute(query).all()
            list_student_history = [
                StudentHistoryMapper.to_history_detail(data) for data in data_row
            ]
            return list_student_history
        except IntegrityError as e:
            self.db_session.rollback()
            raise e
        except Exception as e:
            self.db_session.rollback()
            raise e