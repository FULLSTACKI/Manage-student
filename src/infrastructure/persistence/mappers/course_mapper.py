from src.infrastructure.persistence.models import CourseModel
from src.domain.entities import Course

def _to_model(entity: Course) -> CourseModel:
    return CourseModel(
        course_id=entity.course_id,
        course_name=entity.course_name,
        credits=entity.credits,
        start_course=entity.start_course,
        end_course=entity.end_course,
        department_id=entity.department_id
    )
    
def _to_entity(model: CourseModel) -> Course:
    return Course(
        course_id=model.course_id,
        course_name=model.course_name,
        credits=model.credits,
        start_course=model.start_course,
        end_course=model.end_course,
        department_id=model.department_id
    )