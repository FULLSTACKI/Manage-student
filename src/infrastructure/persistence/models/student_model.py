from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    

class StudentModel(Base):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.department_id"), primary_key=True)
    
    department = relationship("DepartmentModel", back_populates="students")
    scores = relationship("ScoreModel", back_populates="student")
    registrations = relationship("RegistrationModel", back_populates="student", cascade="all, delete-orphan")