from pydantic import BaseModel
from typing import *
from datetime import date as Date
from src.domain.entities import Course

#define course data models
class courseOut(BaseModel):
    id: str
    name: str
    credits: int
    start_course: Date
    end_course: Date
    department_id: str
    
    def from_entity(course: Course):
        
        return courseOut(
            id = course.id,
            name = course.name,
            credits=course.credits,
            start_course=course.start_course,
            end_course=course.end_course,
            department_id=course.department_id           
        )
        
class UploadCourseRequest(BaseModel):
    id: str
    name: str
    credits: int
    start_course: Optional[str]
    end_course: Optional[str] = None
    department_id: str

class UploadCourseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    course: Optional[courseOut] = None
    
class GetCourseRequest(BaseModel):
    id: str

class GetCourseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    course: Optional[courseOut] = None