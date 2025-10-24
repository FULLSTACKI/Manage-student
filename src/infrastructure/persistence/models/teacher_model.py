from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.db import Base

class TeacherModel(Base):
    __tablename__ = "teachers"

    teacher_id = Column(String, primary_key=True, index=True)
    teacher_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    birthday = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.department_id"), nullable=False)

    # Relationships
    department = relationship("DepartmentModel", back_populates="teachers")
    classrooms = relationship("ClassroomModel", back_populates="teacher")