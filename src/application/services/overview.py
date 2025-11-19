from src.domain.repositories import IsOverviewKpiRepo
from src.application.dtos.overview_dto import OverviewKpiResponse, OverviewTopStudent
from src.utils import ValidationError
from typing import List

class OverviewManagement:
    def __init__(self, overview_repo: IsOverviewKpiRepo):
        self.overview_repo = overview_repo
        
    def get_important_kpi(self) -> OverviewKpiResponse:
        try: 
            kpi_data = self.overview_repo.get_all_kpi()
        
            if kpi_data is None:
                raise ValidationError("DB_ERROR: Could not fetch KPI data")
                
            return kpi_data
        except Exception as e:
            raise e
    
    def get_top3_student(self) -> List[OverviewTopStudent]:
        try:
            top3_student = self.overview_repo.get_top3_student()
        
            if top3_student is None: 
                raise ValidationError("DB_ERROR: Could not fetch KPI data")
            
            return top3_student
        except Exception as e:
            raise e
        
    def view_detail_all(self):
        kpi = self.get_important_kpi()
        top3_student = self.get_top3_student()
        return kpi, top3_student