from pydantic import BaseModel, validator
from typing import *
from datetime import date as Date
from src.domain.entities import Student

#Define student data models
class studentOut(BaseModel):
    id: str
    name: str
    email: str
    birthday: Date
    age: int
    sex: str

    def from_entity(student: Student):
        
        return studentOut(
            id = student.id,
            name = student.name,
            email = student.email,
            birthday = student.birthday,
            age = student.age,
            sex = student.sex
        )
        
    
class UploadStudentRequest(BaseModel):
    id: str
    name: str
    email: str
    birthday: Optional[str]
    age: Optional[int] = None
    sex: str
    

class UploadStudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None

class GetStudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None