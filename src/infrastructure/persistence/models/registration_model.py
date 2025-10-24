from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base  
  
class RegistrationModel(Base):
    __tablename__ = "registrations"
    student_id = Column(String, ForeignKey("students.student_id"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.course_id"), primary_key=True)
    registered_at = Column(Date, nullable=False)

    student = relationship("StudentModel", back_populates="registrations")
    course = relationship("CourseModel", back_populates="registrations")
