from abc import ABC, abstractmethod
from src.domain.entities.dtos import AnalyticMetricDTO
from typing import List

class IsAnalyticRepo(ABC):
    # phân tích theo department
    @abstractmethod
    def get_total_student_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod 
    def get_total_student_sex_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_max_gpa_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_min_gpa_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_avg_gpa_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_avg_final_grade_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_total_course_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_min_final_grade_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_max_final_grade_by_department(self) -> List[AnalyticMetricDTO] | None:
        pass
    
    # phân tích theo course
    @abstractmethod
    def get_avg_gpa_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_max_gpa_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_min_gpa_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_avg_final_grade_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_max_final_grade_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_min_final_grade_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_total_student_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_total_department_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_total_student_sex_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_std_gpa_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass
    @abstractmethod
    def get_std_final_grade_by_course(self) -> List[AnalyticMetricDTO] | None:
        pass