from sqlalchemy import Column, String, Float, ForeignKey, UUID   
import uuid
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    

class ScoreModel(Base):
    __tablename__ = "scores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(String, ForeignKey("students.student_id"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.course_id"), primary_key=True)
    coursework_grade = Column(Float, nullable=False)
    midterm_grade = Column(Float, nullable=False)
    final_grade = Column(Float, nullable=False)
    gpa = Column(Float, nullable=False)

    student = relationship("StudentModel", back_populates="scores")
    course = relationship("CourseModel", back_populates="scores")