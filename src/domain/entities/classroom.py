from datetime import date
from src.domain.services import compute_end_course, parse_date

class Classroom:
    def __init__(self, class_id: str, semester: str, academic_year: str, start_time: date, end_time: date, course_id: str, teacher_id: str):
        self.class_id = class_id
        self.semester = semester
        self.academic_year = academic_year
        self.start_time = start_time
        self.end_time = end_time
        self.course_id = course_id
        self.teacher_id = teacher_id

    @classmethod
    def add(cls, class_id: str, semester: str, academic_year: str, start_time: date, duration_weeks: int, course_id: str, teacher_id: str):
        try:
            start_time = parse_date(start_time)
            end_time = compute_end_course(start_time, duration_weeks)
            return cls(
                class_id=class_id,
                semester=semester,
                academic_year=academic_year,
                start_time=start_time,
                end_time=end_time,
                course_id=course_id,
                teacher_id=teacher_id
            )
        except Exception as e: 
            raise e 