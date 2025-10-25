from dataclasses import dataclass
from typing import *
from datetime import date

# Analytic DTO
@dataclass 
class AnalyticMetricDTO:
    column_categorical:str
    column_numerical: Union[int,float]

# DTO tổng quan kpi quan trọng 
@dataclass
class OverviewKpi:
    total_student: int
    total_course: int 
    avg_gpa: float
    
@dataclass 
class OverviewTopStudent:
    student_id: str
    student_name: str
    birthday: date
    gpa: float 
    department_name: str
    
@dataclass 
class Chart:
    chart_type: str 
    data: List[AnalyticMetricDTO] | None
    column_x: str
    column_y: str
    
@dataclass 
class Option:
    id:str
    name:str
    
@dataclass
class StudentDetail:
    student_id: str
    student_name: str
    email: str
    birthday: str
    department_name: str
    course_name: str
    