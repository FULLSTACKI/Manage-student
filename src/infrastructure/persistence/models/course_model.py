from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    start_course = Column(Date, nullable=False)
    end_course = Column(Date, nullable=False)
    department_id = Column(String, ForeignKey("departments.department_id"), primary_key=True)

    department = relationship("Department", back_populates="courses")
    scores = relationship("Score", back_populates="course")
    registrations = relationship("Registration", back_populates="course", cascade="all, delete-orphan")