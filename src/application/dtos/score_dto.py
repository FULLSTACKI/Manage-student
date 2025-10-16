from pydantic import BaseModel
from typing import *
from src.domain.entities import Score

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