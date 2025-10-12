import pandas as pd
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError

from src.database.db import SessionLocal
from src.models.models import Student, Course, Registration
from src.app.service.compare_date_service import parse_date
from src.app.service.age_service import compute_age

DATA_DIR = Path(__file__).parent.parent / "data"

def seed_data_from_csv(db):
    try:
        # 1️⃣ Seed Courses
        course_file = DATA_DIR / "courses.csv"
        if course_file.exists():
            df_courses = pd.read_csv(course_file)
            for _, row in df_courses.iterrows():
                if pd.isna(row.get("id")):
                    continue
                course = Course(
                    id=row.get("id"),
                    name=row.get("name"),
                    credits=int(row.get("credits", 0)),
                    start_course=parse_date(row.get("start_course", "")),
                    end_course=parse_date(row.get("end_course", "")),
                )
                db.merge(course)
        
        # 2️⃣ Seed Students
        students_file = DATA_DIR / "students.csv"
        if students_file.exists():
            df_students = pd.read_csv(students_file)
            for _, row in df_students.iterrows():
                if pd.isna(row.get("id")):
                    continue
                student = Student(
                    id=row.get("id"),
                    name=row.get("name"),
                    birthday=parse_date(row.get("birthday", "")),
                    email=row.get("email"),
                    sex=row.get('sex', ''),
                    age = compute_age(parse_date(row.get("birthday", "")))
                )
                db.merge(student)

        # 3️⃣ Seed Registrations
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