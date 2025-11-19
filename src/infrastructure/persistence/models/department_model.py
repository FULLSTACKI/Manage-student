from sqlalchemy import Column, String, UUID
import uuid
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    

class DepartmentModel(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_id = Column(String, unique=True, index=True, nullable=False)
    department_name = Column(String, nullable=False)
    
    students = relationship("StudentModel", back_populates="department")
    courses = relationship("CourseModel", back_populates="department")
    teachers = relationship("TeacherModel", back_populates="department")