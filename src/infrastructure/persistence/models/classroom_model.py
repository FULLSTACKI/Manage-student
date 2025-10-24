from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base

class ClassroomModel(Base):
    __tablename__ = "classrooms"

    class_id = Column(String, primary_key=True, index=True)
    semester = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)
    start_time = Column(Date, nullable=False)
    end_time = Column(Date, nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.teacher_id"), nullable=False)

    # Relationships
    teacher = relationship("TeacherModel", back_populates="classrooms")
    course = relationship("CourseModel", back_populates="classrooms")
