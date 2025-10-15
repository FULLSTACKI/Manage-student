from pydantic import BaseModel
from typing import *
from datetime import date as Date
from src.domain.entities.students.student import Student
from src.domain.entities.courses.course import Course
from src.domain.entities.scores.score import Score
from src.domain.entities.department.department import Department

# Define score data models
class ScoreOut(BaseModel):
    student_id: str
    course_id: str  
    coursework_grade: float
    midterm_grade: float
    final_grade: float
    gpa: float
    
    def from_entity(score: Score):
        return ScoreOut(
            student_id=score.student_id,
            course_id=score.course_id,
            coursework_grade=score.coursework_grade,
            midterm_grade=score.midterm_grade,
            final_grade=score.final_grade,
            gpa=score.gpa
        )
    
class UploadScoreRequest(BaseModel):
    student_id: str
    course_id: str
    coursework_grade: float
    midterm_grade: float
    final_grade: float
    gpa: Optional[float] = 0.0

class UploadScoreResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    score: Optional[ScoreOut] = None


class GetScoreRequest(BaseModel):
    student_id: str
    course_id: str


class GetScoreResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    score: Optional[ScoreOut] = None 

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
    
class GetStudentRequest(BaseModel):
    id: str

class GetStudentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    student: Optional[studentOut] = None
    
#define course data models
class courseOut(BaseModel):
    id: str
    name: str
    credits: int
    start_course: Date
    end_course: Date
    
    def from_entity(course: Course):
        
        return courseOut(
            id = course.id,
            name = course.name,
            credits=course.credits,
            start_course=course.start_course,
            end_course=course.end_course            
        )
        
class UploadCourseRequest(BaseModel):
    id: str
    name: str
    credits: int
    start_course: Optional[str]
    end_course: Optional[str] = None

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
    
#define department data models
class departmentOut(BaseModel):
    id: str
    name: str
    
    def from_entity(department: Department):
        
        return departmentOut(
            id = department.department_id,
            name = department.department_name,
        )
        
class UploadDepartmentRequest(BaseModel):
    id: str
    name: str

class UploadDepartmentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    department: Optional[departmentOut] = None
    
class GetDepartmentRequest(BaseModel):
    id: str

class GetDepartmentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    department: Optional[departmentOut] = None
    
# Analytics View 
class DimensionDTO(BaseModel):
    key: str
    display: str
    valid_metrics: List[str]
    
class MetricDTO(BaseModel):
    key: str
    display: str
    allowed_agg: List[str]
    
class AnalyticsViewDTO(BaseModel):
    display_name: str
    dimensions: List[DimensionDTO]
    metrics: List[MetricDTO]

# Analytics request 
class AnalyticsRequest(BaseModel):
    dimension: str
    metric: str
    agg: str
    

    