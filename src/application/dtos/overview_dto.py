from pydantic import BaseModel
from typing import *

class OverviewKpiResponse(BaseModel):
    total_student: str
    total_course: str 
    avg_gpa: str
    
class OverviewTopStudent(BaseModel):
    student_id:str
    student_name:str
    birthday:str
    gpa:str
    department_name: str
    
class OverviewResponse(BaseModel):
    kpi: Optional[OverviewKpiResponse] | None
    top3_student: List[OverviewTopStudent] | None