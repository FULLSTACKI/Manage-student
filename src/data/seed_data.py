import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from src.infrastructure.persistence.db import SessionLocal
from src.infrastructure.persistence.models import *
from src.domain.services.hash import _hash_password
from src.domain.services.generate_id import *
from src.domain.services import *
from src.config import SEED_DIR, Role

def seed_data_from_csv(db):
    try:
        # Seed Courses
        course_file = SEED_DIR / "courses.csv"
        if course_file.exists():
            df_courses = pd.read_csv(course_file)
            for _, row in df_courses.iterrows():
                if pd.isna(row.get("course_id")):
                    continue
                course = CourseModel(
                    course_id=row.get("course_id"),
                    course_name=row.get("course_name"),
                    credits=int(row.get("credits", 0)),
                    start_course=parse_date(row.get("start_course", "")),
                    end_course=parse_date(row.get("end_course", "")),
                    department_id = row.get("department_id")
                )
                db.merge(course)
        
        # Seed Students
        students_file = SEED_DIR / "students.csv"
        if students_file.exists():
            df_students = pd.read_csv(students_file)
            for _, row in df_students.iterrows():
                if pd.isna(row.get("student_id")):
                    continue
                student = StudentModel(
                    student_id=row.get("student_id", ""),
                    student_name=row.get("student_name", ""),
                    birthday=parse_date(row.get("birthday", "")),
                    age= compute_age(parse_date(row.get("birthday", ""))),
                    email=row.get("email", ""),
                    sex=row.get('sex', ''),
                    department_id = row.get("department_id", ""),
                    birthplace=row.get("birthplace", ""),
                    address=row.get("address", ""),
                    phone=row.get("phone", ""),
                    ethnicity=row.get("ethnicity", ""),
                    religion=row.get("religion", ""),
                    id_card=row.get("id_card", ""),
                    issue_date=parse_date(row.get("issue_date", "")),
                    issue_place=row.get("issue_place", "")
                )
                db.merge(student)
                
        # Seed Departments
        department_file = SEED_DIR / "departments.csv"
        if department_file.exists():
            df_departments = pd.read_csv(department_file)
            for _, row in df_departments.iterrows():
                if pd.isna(row.get("department_id")):
                    continue
                department = DepartmentModel(
                    department_id = row.get("department_id"),
                    department_name = row.get("department_name")
                )
                db.merge(department)
        
        # Seed Scores
        score_file = SEED_DIR / "scores.csv"
        if score_file.exists():
            df_scores = pd.read_csv(score_file)
            for _, row in df_scores.iterrows():
                if pd.isna(row.get("student_id")) or pd.isna(row.get("course_id")):
                    continue
                score = ScoreModel(
                    student_id = row.get("student_id"),
                    course_id = row.get("course_id"),
                    coursework_grade = row.get("coursework_grade"),
                    midterm_grade = row.get("midterm_grade"),
                    final_grade = row.get("final_grade"),
                    gpa = compute_gpa(row.get("coursework_grade"), row.get("midterm_grade"), row.get("final_grade"))
                )
                db.merge(score)
        

        # Seed Registrations
        registration_file = SEED_DIR / "registrations.csv"
        if registration_file.exists():   
            df_registrations = pd.read_csv(registration_file)
            for _, row in df_registrations.iterrows():
                if pd.isna(row.get("student_id")) or pd.isna(row.get("course_id")):
                    continue
                registration = RegistrationModel(
                    student_id=row.get("student_id"),
                    course_id=row.get("course_id"),
                    registered_at=parse_date(row.get("registered_at", ""))
                )
                db.merge(registration)
                
        # Seed teachers
        teacher_file = SEED_DIR / "teachers.csv"
        if teacher_file.exists():   
            df_teachers = pd.read_csv(teacher_file)
            for _, row in df_teachers.iterrows():
                if pd.isna(row.get("teacher_id")):
                    continue
                teacher = TeacherModel(
                    teacher_id=row.get("teacher_id"),
                    teacher_name=row.get("teacher_name"),
                    email=row.get("email"),
                    birthday=parse_date(row.get("birthday", "")),
                    age=compute_age(parse_date(row.get("birthday", ""))),
                    sex=row.get("sex"),
                    department_id=row.get("department_id")
                )
                db.merge(teacher)
                
        # Seed classrooms
        classroom_file = SEED_DIR / "classrooms.csv"
        if classroom_file.exists():
            df_classrooms = pd.read_csv(classroom_file)
            for _, row in df_classrooms.iterrows():
                if pd.isna(row.get("class_id")) or pd.isna(row.get("course_id")) or pd.isna(row.get("teacher_id")):
                    continue
                classroom = ClassroomModel(
                    class_id = row.get("class_id"),
                    course_id = row.get("course_id"),
                    teacher_id = row.get("teacher_id"),
                    semester = row.get("semester"),
                    academic_year = row.get("academic_year"),
                    start_time = parse_date(row.get("start_time")),
                    end_time = compute_end_course(parse_date(row.get("start_time")))
                )
                db.merge(classroom)
                
        # Seed account
        account_file = SEED_DIR / "account.csv"
        if account_file.exists():   
            df_accounts = pd.read_csv(account_file)
            for _, row in df_accounts.iterrows():
                if pd.isna(row.get("username")):
                    continue
                account = AccountModel(
                    username=row.get("username"),
                    role=Role(row.get("role")),
                    password=_hash_password(row.get("password")),
                    student_id=row.get("student_id",""),
                    teacher_id=row.get("teacher_id","")
                )
                db.merge(account)
                   
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
        student_count = db.query(StudentModel).count()
        if student_count == 0:
            seed_data_from_csv(db)
        else:
            print("Database already has data, skipping seeding.")
    except SQLAlchemyError as e:
        print(f"❌ Error checking data: {e}")
    finally:
        db.close()