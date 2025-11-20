from sqlalchemy import Column, String, ForeignKey, Date, UUID
import uuid
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base

class RegistrationModel(Base):
    __tablename__ = "registrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(String, ForeignKey("students.student_id"), index=True, nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), index=True, nullable=False)
    registered_at = Column(Date, nullable=False)

    student = relationship("StudentModel", back_populates="registrations")
    course = relationship("CourseModel", back_populates="registrations")
