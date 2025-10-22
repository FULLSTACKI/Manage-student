from sqlalchemy.orm import Session
from fastapi import Depends 
from src.infrastructure.persistence.db import get_db
from src.domain.repositories import *
from src.infrastructure.persistence.repositories import *
from src.application.services import *

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

def get_department_repo(db:Session=Depends(get_db)) -> IsDepartmentRepo:
    return DepartmentRepo(db_session=db)

def get_analytic_repo(db:Session=Depends(get_db)) -> IsAnalyticRepo:
    return AnalyticRepo(db_session=db)

def get_analytic_department_service(analytic_repo: IsAnalyticRepo=Depends(get_analytic_repo)) -> AnalyticManagement:
    return AnalyticManagement(analytic_repo=analytic_repo)

def get_overview_repo(db_session: Session= Depends(get_db)) -> IsOverviewKpiRepo:
    return OverviewRepo(db_session=db_session)

def get_overview_service(overview_repo: IsOverviewKpiRepo = Depends(get_overview_repo)) -> OverviewManagement:
    return OverviewManagement(overview_repo=overview_repo)