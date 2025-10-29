from pydantic import BaseModel
from typing import *
from src.domain.entities import StudentDetail

#Define student data models
class studentOut(BaseModel):
    student_id: str
    student_name: str
    email: str
    age: str
    birthday: str
    sex: str
    departments: Optional[str] = None
    courses: Optional[str] = None

    def from_entity(student: StudentDetail):
        return studentOut(
            student_id = student.student_id,
            student_name = student.student_name,
            email = student.email,
            age = f"{student.age}",
            birthday = f"{student.birthday}",
            sex = student.sex,
            departments=student.department_name,
            courses=student.course_name
        )
        
    
class UploadStudentRequest(BaseModel):
    id: str
    name: str
    email: str
    birthday: str
    age: str = None
    sex: str
    department_id: str
    

class StudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None
    
class Option(BaseModel): 
    id: str
    name: str 
    
class StudentFilterOption(BaseModel):
    departments: List[Option] = None
    courses: List[Option] = None
    
class StudentDetailRequest(BaseModel):
    columns: List[str] 
    department_id: List[str] = None
    course_id: List[str] = None