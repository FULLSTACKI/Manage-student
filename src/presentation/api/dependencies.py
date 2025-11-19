from sqlalchemy.orm import Session
from fastapi import Depends 
from fastapi.security import OAuth2PasswordBearer
from src.infrastructure.persistence.db import get_db
from src.domain.repositories import *
from src.infrastructure.persistence.repositories import *
from src.infrastructure.persistence.visualization import SeabornChartService
from src.infrastructure.persistence.agent import GeminiInsightService
from src.infrastructure.persistence.export import *
from src.application.auth.auth_service import AuthorizationService
from src.application.services import *
from src.domain.entities.account import Account
from fastapi import HTTPException

def get_student_command_repo(db_session: Session =Depends(get_db)) -> IsStudentCommandRepo:
    return StudentCommandRepo(db_session=db_session)
def get_student_query_repo(db_session: Session =Depends(get_db)) -> IsStudentQueryRepo:
    return StudentQueryRepo(db_session=db_session)
def get_student_history_repo(db_session: Session =Depends(get_db)) -> IsStudentHistoryRepo:
    return StudentHistoryRepo(db_session=db_session)
def get_course_repo(db_session: Session =Depends(get_db)) -> IsCourseRepo:
    return CourseRepo(db_session=db_session)
def get_score_repo(db_session: Session =Depends(get_db)) -> IsScoreRepo:
    return ScoreRepo(db_session=db_session)
def get_registration_repo(db_session: Session =Depends(get_db)) -> IsRegistrationRepo:
    return RegistrationRepo(db_session=db_session)
def get_department_repo(db:Session=Depends(get_db)) -> IsDepartmentRepo:
    return DepartmentRepo(db_session=db)
def get_analytic_repo(db:Session=Depends(get_db)) -> IsAnalyticRepo:
    return AnalyticRepo(db_session=db)
def get_overview_repo(db_session: Session= Depends(get_db)) -> IsOverviewKpiRepo:
    return OverviewRepo(db_session=db_session)
def get_account_repo(db_session: Session = Depends(get_db)) -> IsAccountRepo:
    return AccountRepo(db_session=db_session)
def get_session_token_repo(db_session: Session = Depends(get_db)) -> IsSessionTokenRepo:
    return SessionTokenRepo(db_session=db_session)

def get_auth_service() -> AuthorizationService:
    return AuthorizationService()
def get_account_service(
    account_repo: IsAccountRepo = Depends(get_account_repo),
    token_repo: IsSessionTokenRepo = Depends(get_session_token_repo)
    ) -> AccountManagement:
    return AccountManagement(account_repo=account_repo, token_repo=token_repo)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AccountManagement = Depends(get_account_service)
) -> Account:
    try:
        user = service.get_current_user(token)
        return user
    except ValidationError as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def require_role(allowed_roles: list[str]):
    def role_check(student_id: str = None, current_account: Account = Depends(get_current_user), auth_service: AuthorizationService = Depends(get_auth_service)):
        auth_service.check_permission_role(current_account, allowed_roles, student_id)
    return role_check

def get_export_service() -> dict[str, IsExportFile]:
    return {
        ".xlsx": ExcelExportFile(),
        ".docx": DocxExportFile()
    }
    
def get_student_command_service(student_repo: IsStudentCommandRepo = Depends(get_student_command_repo)) -> StudentCommandManagement:
    return StudentCommandManagement(student_repo=student_repo)
def get_student_history_service(student_history_repo: IsStudentHistoryRepo = Depends(get_student_history_repo)) -> StudentHistoryManagement:
    return StudentHistoryManagement(repo_student_history=student_history_repo)
def get_student_import_file_service(student_repo: IsStudentCommandRepo = Depends(get_student_command_repo)) -> StudentImportFileManagement:
    return StudentImportFileManagement(student_repo=student_repo)
def get_student_query_service(
    student_repo: IsStudentQueryRepo = Depends(get_student_query_repo),
    course_repo: IsCourseRepo = Depends(get_course_repo),
    department_repo: IsDepartmentRepo = Depends(get_department_repo),
    ) -> StudentQueryManagement:
    return StudentQueryManagement(
        student_query_repo=student_repo,
        course_repo=course_repo,
        department_repo=department_repo,
    )
    
def get_course_service(course_repo: IsCourseRepo = Depends(get_course_repo)) -> CourseManagement:
    return CourseManagement(course_repo=course_repo)

def get_score_service(regis_repo: IsRegistrationRepo = Depends(get_registration_repo), score_repo: IsScoreRepo = Depends(get_score_repo)) -> ScoreManagement:
    return ScoreManagement(score_repo=score_repo, regis_repo=regis_repo)

def get_analytic_service(
    analytic_repo: IsAnalyticRepo=Depends(get_analytic_repo),
    chart_service: IsChartService=Depends(SeabornChartService),
    insight_service: IsInsightService=Depends(GeminiInsightService),
    export_service: dict[str, IsExportFile]=Depends(get_export_service)
    ) -> AnalyticManagement:
    return AnalyticManagement(
        analytic_repo=analytic_repo,
        chart_service=chart_service,
        insight_service=insight_service,
        export_service=export_service
    )

def get_overview_service(overview_repo: IsOverviewKpiRepo = Depends(get_overview_repo)) -> OverviewManagement:
    return OverviewManagement(overview_repo=overview_repo)