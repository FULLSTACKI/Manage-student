from pydantic import BaseModel
from datetime import date
from typing import *

class studentOut(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    birthday: Optional[date] = None
    sex: Optional[str] = None 
    departments: Optional[str] = None
    courses: Optional[str] = None
    birthplace: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    id_card: Optional[str] = None
    issue_date: Optional[date] = None
    issue_place: Optional[str] = None
    
class StudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None

class Option(BaseModel):
    id: str
    name: str

class StudentFilterOption(BaseModel):
    departments: Optional[List[Option]] = None
    courses: Optional[List[Option]] = None

class StudentDetailRequest(BaseModel):
    columns: List[str]
    department_id: Optional[List[str]] = None
    course_id: Optional[List[str]] = None
