from sqlalchemy import Column, String, Integer, ForeignKey, Date, UUID
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base    
import uuid

class StudentModel(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
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
    department_id = Column(String, ForeignKey("departments.department_id"), nullable=False, index=True)
    
    # --- 5. RELATIONSHIPS ---
    department = relationship("DepartmentModel", back_populates="students")
    scores = relationship("ScoreModel", back_populates="student", cascade="all, delete-orphan")
    registrations = relationship("RegistrationModel", back_populates="student", cascade="all, delete-orphan")
    account = relationship("AccountModel", back_populates="student")
    histories = relationship("StudentHistoryModel", back_populates="student", cascade="all, delete-orphan")