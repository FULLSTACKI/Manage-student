from .students import router as student_router
from .scores import router as score_router
from .analytics import router as analytic_router
from .courses import router as course_router 
from .overview import router as overview_router

list_routers = [
    student_router,
    course_router,
    score_router,
    analytic_router,
    overview_router
]