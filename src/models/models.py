from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base    

class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)

    scores = relationship("Score", back_populates="student")
    registrations = relationship("Registration", back_populates="student", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    start_course = Column(Date, nullable=False)
    end_course = Column(Date, nullable=False)

    scores = relationship("Score", back_populates="course")
    registrations = relationship("Registration", back_populates="course", cascade="all, delete-orphan")

class Score(Base):
    __tablename__ = "scores"
    student_id = Column(String, ForeignKey("students.id"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"), primary_key=True)
    coursework_grade = Column(Float, nullable=False)
    midterm_grade = Column(Float, nullable=False)
    final_grade = Column(Float, nullable=False)
    gpa = Column(Float, nullable=False)

    student = relationship("Student", back_populates="scores")
    course = relationship("Course", back_populates="scores")


class Registration(Base):
    __tablename__ = "registrations"
    student_id = Column(String, ForeignKey("students.id"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"), primary_key=True)
    registered_at = Column(Date, nullable=False)

    student = relationship("Student", back_populates="registrations")
    course = relationship("Course", back_populates="registrations")
