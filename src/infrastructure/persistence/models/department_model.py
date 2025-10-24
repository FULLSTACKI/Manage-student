from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    

class DepartmentModel(Base):
    __tablename__ = "departments"
    department_id = Column(String, primary_key=True)
    department_name = Column(String, nullable=False)
    
    students = relationship("StudentModel", back_populates="department")
    courses = relationship("CourseModel", back_populates="department")
    teachers = relationship("TeacherModel", back_populates="department")