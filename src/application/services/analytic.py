from src.domain.repositories.analytic_repo import IsAnalyticRepo
from src.application.dtos import *
from src.utils import ValidationError, HTTPException
from typing import *

class AnalyticManagement:
    def __init__(self, analytic_repo: IsAnalyticRepo):
        self.analytic_repo = analytic_repo
        
        self._analytics_map: Dict[Tuple[str, str, str], Callable[[],List[Dict]]] = {
            ('department', 'course', 'count'): 
                self.analytic_repo.get_total_course_by_department,
            
            ('department', 'student', 'count'): 
                self.analytic_repo.get_total_student_by_department,
            
            ('department', 'sex', 'count'): 
                self.analytic_repo.get_total_student_sex_by_department,
            
            ('department', 'gpa','avg'): 
                self.analytic_repo.get_avg_gpa_by_department,
            
            ('department', 'gpa','min'): 
                self.analytic_repo.get_min_gpa_by_department,
            
            ('department', 'gpa','max'): 
                self.analytic_repo.get_max_gpa_by_department,
            
            ('department', 'final grade','avg'): 
                self.analytic_repo.get_avg_final_grade_by_department,
            
            ('department', 'final grade','min'): 
                self.analytic_repo.get_min_final_grade_by_department,
            
            ('department', 'final grade','max'): 
                self.analytic_repo.get_max_final_grade_by_department,
                
            ('course', 'final grade','max'): 
                self.analytic_repo.get_max_final_grade_by_course,
                
            ('course', 'final grade','min'): 
                self.analytic_repo.get_min_final_grade_by_course,
                
            ('course', 'final grade','avg'): 
                self.analytic_repo.get_avg_final_grade_by_course,
                
            ('course', 'final grade','std'): 
                self.analytic_repo.get_std_final_grade_by_course,
                
            ('course', 'gpa','max'): 
                self.analytic_repo.get_max_gpa_by_course,
                
            ('course', 'gpa','min'): 
                self.analytic_repo.get_min_gpa_by_course,
                
            ('course', 'gpa','avg'): 
                self.analytic_repo.get_avg_gpa_by_course,
                
            ('course', 'gpa','std'): 
                self.analytic_repo.get_std_gpa_by_course,
            
            ('course', 'student','count'): 
                self.analytic_repo.get_total_student_by_course,
                
            ('course', 'department','count'): 
                self.analytic_repo.get_total_department_by_course,
                
            ('course', 'sex','count'): 
                self.analytic_repo.get_total_student_sex_by_course,
                
        }
        
    def get_analytic_department_view(self, req:AnalyticsRequest) -> List[AnalyticsResponse]:
        try:
            query_map = (req.dimension, req.metric, req.agg)
            query_funct = self._analytics_map.get(query_map)
            if not query_funct:
                raise HTTPException(
                    status_code=400,
                    detail=f"Sự kết hợp truy vấn không được hỗ trợ: {query_map}"
                )
            raw_data = query_funct()
            result_dtos = [AnalyticsResponse(columns_x=row.column_categorical, columns_y=f"{row.column_numerical:.2f}") for row in raw_data]
            return result_dtos
        except ValidationError as e:
            raise e
        except Exception as e:
            raise e