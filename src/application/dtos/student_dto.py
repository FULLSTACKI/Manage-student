from pydantic import BaseModel
from typing import *
from datetime import date as Date
from src.domain.entities import Student

#Define student data models
class studentOut(BaseModel):
    id: str
    name: str
    email: str
    birthday: str
    age: str
    sex: str
    department_id: str

    def from_entity(student: Student):
        return studentOut(
            id = student.student_id,
            name = student.student_name,
            email = student.email,
            birthday = f"{student.birthday}",
            age = f"{student.age}",
            sex = student.sex,
            department_id=student.department_id
        )
        
    
class UploadStudentRequest(BaseModel):
    id: str
    name: str
    email: str
    birthday: str
    age: str = None
    sex: str
    department_id: str
    

class UploadStudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None

class GetStudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None
    
class Option(BaseModel): 
    id: str
    name: str 
    
class StudentFilterOption(BaseModel):
    departments: List[Option] = None
    courses: List[Option] = None