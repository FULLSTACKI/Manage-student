from .student_command import router as student_command_router
from .student_history import router as student_history_router
from .student_import_file import router as student_import_file_router
from .student_query import router as admin_student_query_router
from .view_config import router as view_config_router
from .scores import router as score_router
from .analytics import router as analytic_router
from .courses import router as course_router 
from .overview import router as overview_router
from .auth import router as account_router

list_routers = [
    student_command_router,
    student_history_router,
    student_import_file_router,
    admin_student_query_router,
    view_config_router,
    course_router,
    score_router,
    analytic_router,
    overview_router,
    account_router
]