from sqlalchemy import Column, String, ForeignKey,UUID
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base
import uuid

class AccountModel(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    student_id = Column(String, ForeignKey("students.id"), nullable=True)
    teacher_id = Column(String, ForeignKey("teachers.id"), nullable=True) 
    

    student = relationship("StudentModel", back_populates="account")
    teacher = relationship("TeacherModel", back_populates="account") 