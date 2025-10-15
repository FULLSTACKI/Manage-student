import pandas as pd
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError

from src.database.db import SessionLocal
from src.models.models import Student, Course, Registration, Score, Department
from src.app.service.compare_date_service import parse_date
from src.app.service.age_service import compute_age
from src.app.service.gpa_service import compute_gpa

DATA_DIR = Path(__file__).parent.parent / "data"

def seed_data_from_csv(db):
    try:
        # Seed Courses
        course_file = DATA_DIR / "courses.csv"
        if course_file.exists():
            df_courses = pd.read_csv(course_file)
            for _, row in df_courses.iterrows():
                if pd.isna(row.get("course_id")):
                    continue
                course = Course(
                    course_id=row.get("course_id"),
                    course_name=row.get("course_name"),
                    credits=int(row.get("credits", 0)),
                    start_course=parse_date(row.get("start_course", "")),
                    end_course=parse_date(row.get("end_course", "")),
                    department_id = row.get("department_id")
                )
                db.merge(course)
        
        # Seed Students
        students_file = DATA_DIR / "students.csv"
        if students_file.exists():
            df_students = pd.read_csv(students_file)
            for _, row in df_students.iterrows():
                if pd.isna(row.get("student_id")):
                    continue
                student = Student(
                    student_id=row.get("student_id"),
                    student_name=row.get("student_name"),
                    birthday=parse_date(row.get("birthday", "")),
                    email=row.get("email"),
                    sex=row.get('sex', ''),
                    age = compute_age(parse_date(row.get("birthday", ""))),
                    department_id = row.get("department_id")
                )
                db.merge(student)
                
        # Seed Departments
        department_file = DATA_DIR / "departments.csv"
        if department_file.exists():
            df_departments = pd.read_csv(department_file)
            for _, row in df_departments.iterrows():
                if pd.isna(row.get("department_id")):
                    continue
                department = Department(
                    department_id = row.get("department_id"),
                    department_name = row.get("department_name")
                )
                db.merge(department)
        
        # Seed Scores
        score_file = DATA_DIR / "scores.csv"
        if score_file.exists():
            df_scores = pd.read_csv(score_file)
            for _, row in df_scores.iterrows():
                if pd.isna(row.get("student_id")) or pd.isna(row.get("course_id")):
                    continue
                score = Score(
                    student_id = row.get("student_id"),
                    course_id = row.get("course_id"),
                    coursework_grade = row.get("coursework_grade"),
                    midterm_grade = row.get("midterm_grade"),
                    final_grade = row.get("final_grade"),
                    gpa = compute_gpa(row.get("coursework_grade"), row.get("midterm_grade"), row.get("final_grade"))
                )
                db.merge(score)
        

        # Seed Registrations
        registration_file = DATA_DIR / "registrations.csv"
        if registration_file.exists():   
            df_registrations = pd.read_csv(registration_file)
            for _, row in df_registrations.iterrows():
                if pd.isna(row.get("student_id")) or pd.isna(row.get("course_id")):
                    continue
                registration = Registration(
                    student_id=row.get("student_id"),
                    course_id=row.get("course_id"),
                    registered_at=parse_date(row.get("registered_at", ""))
                )
                db.merge(registration)
        
        db.commit()
        print("✅ Seeding completed!\n")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()
        
def seed_data_if_empty():
    db = SessionLocal()
    try:
        student_count = db.query(Student).count()
        if student_count == 0:
            seed_data_from_csv(db)
        else:
            print("Database already has data, skipping seeding.")
    except SQLAlchemyError as e:
        print(f"❌ Error checking data: {e}")
    finally:
        db.close()