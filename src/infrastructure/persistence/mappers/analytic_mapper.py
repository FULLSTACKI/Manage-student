from src.infrastructure.persistence.models import StudentModel, CourseModel, DepartmentModel, ScoreModel
# from src.application.dtos.analytic_view_dto import AnalyticsResponse

class AnalyticMapper:
    @staticmethod 
    def map_dimension(dimensions: str):
        map_col = {
            "department": DepartmentModel.department_name,
            "course": CourseModel.course_name,
            "sex": StudentModel.sex
        }
        return map_col.get(dimensions)
    @staticmethod
    def map_metric(metric: str):
        map_col = {
            "student": StudentModel.student_id,
            "gpa": ScoreModel.gpa,
            "final grade": ScoreModel.final_grade,
            "course": CourseModel.course_id,
            "sex": StudentModel.sex
        }
        return map_col.get(metric)
    @staticmethod
    def map_agg(agg: str):
        map_agg = {
            "sum": "sum",
            "avg": "avg",
            "mean": "avg",
            "max": "max",
            "min": "min",
            "count": "count",
            "std": "stddev",
            "var": "variance"
        }
        return map_agg.get(agg)