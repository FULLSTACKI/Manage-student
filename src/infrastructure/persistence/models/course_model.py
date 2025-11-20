from sqlalchemy import Column, String, Integer, ForeignKey, Date, UUID
import uuid
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    

class CourseModel(Base):
    __tablename__ = "courses"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(String,primary_key=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    start_course = Column(Date, nullable=False)
    end_course = Column(Date, nullable=False)
    department_id = Column(String, ForeignKey("departments.department_id"), nullable=False, index=True)

    department = relationship("DepartmentModel", back_populates="courses")
    scores = relationship("ScoreModel", back_populates="course")
    registrations = relationship("RegistrationModel", back_populates="course", cascade="all, delete-orphan")
    classrooms = relationship("ClassroomModel", back_populates="course")