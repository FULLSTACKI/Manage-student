from pydantic import BaseModel
from typing import *
from datetime import date

class OverviewKpiResponse(BaseModel):
    total_student: Optional[float] | None
    total_course: Optional[float] | None
    avg_gpa: Optional[float] | None
    
class OverviewTopStudent(BaseModel):
    student_id:str
    student_name:str
    birthday:Optional[date] | None
    gpa:Optional[float] | None
    department_name: str
    
class OverviewResponse(BaseModel):
    kpi: Optional[OverviewKpiResponse] | None
    top3_student: List[OverviewTopStudent] | None