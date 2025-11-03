from sqlalchemy import Column, String, Integer, Date, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.models.audit_model import AuditBaseModel

class StudentHistoryModel(AuditBaseModel):
    __tablename__ = "student_history"

    student_id = Column(String, ForeignKey("students.student_id"))
    student_name = Column(String)
    email = Column(String)
    birthday = Column(Date)
    sex = Column(String)
    age = Column(Integer)
    department_id = Column(String)
    birthplace = Column(String)
    address = Column(String)
    phone = Column(String)
    ethnicity = Column(String)
    religion = Column(String)
    id_card = Column(String)
    issue_date = Column(String)
    issue_place = Column(String)
    
    student = relationship("StudentModel", back_populates=None)