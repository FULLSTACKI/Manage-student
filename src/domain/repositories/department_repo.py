from abc import ABC, abstractmethod
from src.domain.entities.department import Department
from src.domain.entities.dtos import *
from typing import List

class IsDepartmentRepo(ABC):
    @abstractmethod
    def get_by_id(self, department_id:str) -> Department | None:
        pass
    @abstractmethod
    def get_all(self) -> List[Department] | None:
        pass
    @abstractmethod 
    def get_total_student_by_department(self) -> List[DepartmentStudentCountDTO] | None:
        pass
    @abstractmethod 
    def get_total_student_sex_by_department(self) -> List[DepartmentStudentSexCountDTO] | None:
        pass
    @abstractmethod
    def get_max_gpa_by_department(self) -> List[DepartmentCourseMaxGpaDTO] | None:
        pass
    @abstractmethod
    def get_min_gpa_by_department(self) -> List[DepartmentCourseMinGpaDTO] | None:
        pass
    @abstractmethod
    def get_avg_gpa_by_department(self) -> List[DepartmentCourseAvgGpaDTO] | None:
        pass
    @abstractmethod
    def get_avg_final_grade_by_department(self) -> List[DepartmentCourseAvgFinalGradeDTO] | None:
        pass
    @abstractmethod
    def get_total_course_by_department(self) -> List[DepartmentCourseCountDTO] | None:
        pass
    @abstractmethod
    def get_min_final_grade_by_department(self) -> List[DepartmentCourseMinFinalGradeDTO] | None:
        pass
    @abstractmethod
    def get_max_final_grade_by_department(self) -> List[DepartmentCourseMaxFinalGradeDTO] | None:
        pass
    @abstractmethod
    def save(self, req_department: Department) -> Department | None: 
        pass
    