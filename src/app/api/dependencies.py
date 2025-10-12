from sqlalchemy.orm import Session
from fastapi import Depends 
from src.database.db import get_db
from src.domain.entities.students.student_repo import IsStudentRepo
from src.infrastructure.repo.student_repo import StudentRepo
from src.app.service.student import StudentManagement
from src.domain.entities.courses.course_repo import IsCourseRepo
from src.infrastructure.repo.course_repo import CourseRepo
from src.domain.entities.scores.score_repo import IsScoreRepo
from src.infrastructure.repo.score_repo import ScoreRepo
from src.domain.entities.registrations.registration_repo import IsRegistrationRepo
from src.infrastructure.repo.registration_repo import RegistrationRepo
from src.app.service.course import CourseManagement
from src.app.service.score import ScoreManagement
from src.domain.entities.registrations.registration_repo import IsRegistrationRepo

def get_student_repo(db_session: Session =Depends(get_db)) -> IsStudentRepo:
    return StudentRepo(db_session=db_session)

def get_student_service(student_repo: IsStudentRepo = Depends(get_student_repo)) -> StudentManagement:
    return StudentManagement(student_repo=student_repo)

def get_course_repo(db_session: Session =Depends(get_db)) -> IsCourseRepo:
    return CourseRepo(db_session=db_session)

def get_course_service(course_repo: IsCourseRepo = Depends(get_course_repo)) -> CourseManagement:
    return CourseManagement(course_repo=course_repo)

def get_score_repo(db_session: Session =Depends(get_db)) -> IsScoreRepo:
    return ScoreRepo(db_session=db_session)

def get_registration_repo(db_session: Session =Depends(get_db)) -> IsRegistrationRepo:
    return RegistrationRepo(db_session=db_session)

def get_score_service(regis_repo: IsRegistrationRepo = Depends(get_registration_repo), score_repo: IsScoreRepo = Depends(get_score_repo)) -> ScoreManagement:
    return ScoreManagement(score_repo=score_repo, regis_repo=regis_repo)