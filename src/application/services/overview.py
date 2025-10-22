from src.domain.repositories import IsOverviewKpiRepo
from src.application.dtos.overview_dto import OverviewKpiResponse, OverviewTopStudent
from src.utils import ValidationError
from typing import List

class OverviewManagement:
    def __init__(self, overview_repo: IsOverviewKpiRepo):
        self.overview_repo = overview_repo
        
    def get_important_kpi(self) -> OverviewKpiResponse:
        kpi_data = self.overview_repo.get_all_kpi()
        
        if kpi_data is None:
            raise ValidationError("DB_ERROR: Could not fetch KPI data")
            
        return OverviewKpiResponse(
            total_student=str(kpi_data.total_student),
            total_course=str(kpi_data.total_course),
            avg_gpa=f"{kpi_data.avg_gpa:.2f}"
        )
    
    def get_top3_student(self) -> List[OverviewTopStudent]:
        top3_student = self.overview_repo.get_top3_student()
        
        if top3_student is None: 
            raise ValidationError("DB_ERROR: Could not fetch KPI data")
        
        return [OverviewTopStudent(
            student_id=student.student_id,
            student_name=student.student_name,
            birthday=f"{student.birthday}",
            gpa=f"{student.gpa:.2f}",
            department_name=student.department_name 
        ) for student in top3_student]
        
    def view_detail_all(self):
        kpi = self.get_important_kpi()
        top3_student = self.get_top3_student()
        return kpi, top3_student