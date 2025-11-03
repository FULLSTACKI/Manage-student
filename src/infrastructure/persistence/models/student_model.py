from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    
from src.infrastructure.persistence.auto import AuditMixin
from .student_history_model import StudentHistoryModel

class StudentModel(Base, AuditMixin):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)
    birthplace = Column(String, nullable=False)        
    address = Column(String, nullable=False)           
    phone = Column(String, nullable=False)           
    ethnicity = Column(String, nullable=True)  
    religion = Column(String, nullable=True)                   
    id_card = Column(String,unique=True, nullable=False)          
    issue_date = Column(Date, nullable=False)          
    issue_place = Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.department_id"), primary_key=True)
    
    department = relationship("DepartmentModel", back_populates="students")
    scores = relationship("ScoreModel", back_populates="student", cascade="all, delete-orphan")
    registrations = relationship("RegistrationModel", back_populates="student", cascade="all, delete-orphan")
    
StudentModel.register_audit(StudentHistoryModel)