from sqlalchemy.orm import Session
from src.domain.repositories import IsOverviewKpiRepo
from src.application.dtos.overview_dto import OverviewKpiResponse, OverviewTopStudent
from src.infrastructure.persistence.models import StudentModel, CourseModel, ScoreModel, DepartmentModel
from sqlalchemy import select, func
from typing import List

class OverviewRepo(IsOverviewKpiRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_all_kpi(self) -> OverviewKpiResponse:
        try:
            query = (
                select(
                    func.avg(ScoreModel.gpa).label("avg_gpa"),
                    func.count(StudentModel.student_id).label("total_student"),
                    func.count(CourseModel.course_id).label("total_course")
                ).select_from(StudentModel)
                .join(ScoreModel, StudentModel.student_id == ScoreModel.student_id)
                .join(CourseModel, CourseModel.course_id == ScoreModel.course_id)
            )
            result = self.db_session.execute(query).mappings().first()
            return OverviewKpiResponse(**result)
        except Exception as e:
            raise e  
        
    def get_top3_student(self) -> List[OverviewTopStudent]:
        try:
            query = (
                select(
                    StudentModel.student_id,
                    StudentModel.student_name,
                    StudentModel.birthday,
                    func.avg(ScoreModel.gpa).label("gpa"),
                    DepartmentModel.department_name
                ).select_from(StudentModel)
                .join(ScoreModel, StudentModel.student_id == ScoreModel.student_id)
                .join(DepartmentModel, StudentModel.department_id == DepartmentModel.department_id)
                .group_by(StudentModel.student_id)
                .order_by(func.avg(ScoreModel.gpa).desc())
            )
            row_data = self.db_session.execute(query).mappings().all()
            return [OverviewTopStudent(**data) for data in row_data]
        except Exception as e:
            raise e  