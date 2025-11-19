from sqlalchemy import Column, String, Date, ForeignKey, UUID
import uuid
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base

class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id = Column(String,unique=True, index=True)
    semester = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)
    start_time = Column(Date, nullable=False)
    end_time = Column(Date, nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.teacher_id"), nullable=False)

    # Relationships
    teacher = relationship("TeacherModel", back_populates="classrooms")
    course = relationship("CourseModel", back_populates="classrooms")
