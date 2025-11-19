from sqlalchemy import Column, String, Date, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from src.infrastructure.persistence.db import Base

class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    teacher_id = Column(String, unique=True, index=True)
    teacher_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    birthday = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.department_id"), nullable=False, index=True)
    account = relationship("AccountModel", back_populates="teacher")
    # Relationships
    department = relationship("DepartmentModel", back_populates="teachers")
    classrooms = relationship("ClassroomModel", back_populates="teacher")