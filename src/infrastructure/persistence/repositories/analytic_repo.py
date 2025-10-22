from sqlalchemy.orm import Session
from src.domain.repositories import IsAnalyticRepo
from src.domain.entities.dtos import AnalyticMetricDTO
from sqlalchemy import text
from typing import List

class AnalyticRepo(IsAnalyticRepo):
    def __init__(self, db_session: Session = None):
        self.db = db_session
        
    def get_total_student_sex_by_department(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        d.department_name, 
                        COUNT(CASE WHEN s.sex = 'M' THEN 1 END) AS total_M,
                        COUNT(CASE WHEN s.sex = 'F' THEN 1 END) AS total_F
                    FROM departments as d
                    JOIN students as s ON s.department_id = d.department_id
                    GROUP BY d.department_name
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data[sql_column]
            ) 
            for data in department_row
            for sql_column in ["total_M", "total_F"]]
        except Exception as e:
            raise e
        
    def get_min_final_grade_by_department(self):
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MIN(s.final_grade) as min_final_grade
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY min_final_grade
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["min_final_grade"]
            ) for data in data_row]
        except Exception as e:
            raise  e
        
    def get_max_final_grade_by_department(self):
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MAX(s.final_grade) as max_final_grade
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY max_final_grade DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["max_final_grade"]                
            ) for data in data_row]
        except Exception as e:
            raise  e
        
    def get_total_course_by_department(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        d.department_name, 
                        COUNT(c.course_id) as total_courses
                    FROM departments as d
                    JOIN courses as c ON d.department_id = c.department_id
                    GROUP BY d.department_name
                    ORDER BY total_courses DESC
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_total_student_department = [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["total_courses"]
            ) for data in department_row]
            return list_total_student_department
        except Exception as e:
            raise e
        
    def get_min_gpa_by_department(self) -> List[AnalyticMetricDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MIN(s.gpa) as min_gpa
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY min_gpa 
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["min_gpa"]
            ) for data in data_row]
        except Exception as e:
            raise  e
        
    def get_max_gpa_by_department(self) -> List[AnalyticMetricDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        MAX(s.gpa) as max_gpa
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY max_gpa DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["max_gpa"]    
            ) for data in data_row]
        except Exception as e:
            raise  e
        
    def get_avg_gpa_by_department(self) -> List[AnalyticMetricDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        AVG(s.gpa) as avg_gpa
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY avg_gpa DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["avg_gpa"]
            ) for data in data_row]
        except Exception as e:
            raise e
    
    def get_avg_final_grade_by_department(self) -> List[AnalyticMetricDTO]:
        try: 
            query = text(
                """
                    SELECT 
                        d.department_name,
                        AVG(s.final_grade) as avg_final_grade
                    FROM departments as d 
                    JOIN courses as c ON d.department_id = c.department_id
                    JOIN scores as s ON s.course_id = c.course_id 
                    GROUP BY d.department_name
                    ORDER BY avg_final_grade DESC
                """
            )
            result = self.db.execute(query)
            data_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["avg_final_grade"]
            ) for data in data_row]
        except Exception as e:
            raise  e
        
    def get_total_student_by_department(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        d.department_name, 
                        COUNT(s.student_id) as total_students
                    FROM departments as d
                    JOIN students as s ON d.department_id = s.department_id
                    GROUP BY d.department_name
                    ORDER BY total_students DESC
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            list_total_student_department = [AnalyticMetricDTO(
                column_categorical=data["department_name"],
                column_numerical=data["total_students"]
            ) for data in department_row]
            return list_total_student_department
        except Exception as e:
            raise e
        
    def get_avg_final_grade_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        AVG(s.final_grade) as avg_final_grade
                    FROM courses as c 
                    JOIN scores as s ON c.course_id = s.course_id
                    GROUP BY c.course_name
                    ORDER BY avg_final_grade DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["avg_final_grade"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_min_final_grade_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        MIN(s.final_grade) as min_final_grade
                    FROM courses as c 
                    JOIN scores as s ON c.course_id = s.course_id
                    GROUP BY c.course_name
                    ORDER BY min_final_grade DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["min_final_grade"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_max_final_grade_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        MAX(s.final_grade) as max_final_grade
                    FROM courses as c 
                    JOIN scores as s ON c.course_id = s.course_id
                    GROUP BY c.course_name
                    ORDER BY max_final_grade DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["max_final_grade"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_avg_gpa_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        AVG(s.gpa) as avg_gpa
                    FROM courses as c 
                    JOIN scores as s ON c.course_id = s.course_id
                    GROUP BY c.course_name
                    ORDER BY avg_gpa DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["avg_gpa"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_min_gpa_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        MIN(s.gpa) as min_gpa
                    FROM courses as c 
                    JOIN scores as s ON c.course_id = s.course_id
                    GROUP BY c.course_name
                    ORDER BY min_gpa DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["min_gpa"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_max_gpa_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        MAX(s.gpa) as max_gpa
                    FROM courses as c 
                    JOIN scores as s ON c.course_id = s.course_id
                    GROUP BY c.course_name
                    ORDER BY max_gpa DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["max_gpa"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_total_department_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        COUNT(d.department_id) as total_department
                    FROM courses as c 
                    JOIN departments as d ON d.department_id = c.department_id
                    GROUP BY c.course_name
                    ORDER BY total_department DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["total_department"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_total_student_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        COUNT(r.student_id) as total_student
                    FROM courses as c 
                    JOIN registrations as r ON r.course_id = c.course_id 
                    GROUP BY c.course_name
                    ORDER BY total_student DESC 
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["total_student"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_total_student_sex_by_course(self) -> List[AnalyticMetricDTO]:
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        registration_sex.total_M,
                        registration_sex.total_F
                    FROM courses as c 
                    JOIN 
                        (SELECT 
                            r.course_id,
                            COUNT(CASE WHEN s.sex = 'M' THEN 1 END) AS total_M,
                            COUNT(CASE WHEN s.sex = 'F' THEN 1 END) AS total_F,
                            COUNT(r.student_id) AS total_all_sex
                        FROM registrations as r 
                        JOIN students as s ON r.student_id = s.student_id
                        GROUP BY r.course_id ) as registration_sex 
                    ON registration_sex.course_id = c.course_id 
                    ORDER BY registration_sex.total_all_sex DESC
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data[sql_column]
            ) for data in department_row
            for sql_column in ["total_M", "total_F"]]
        except Exception as e:
            raise e
        
    def get_std_gpa_by_course(self):
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        SQRT(
                            (SUM(s.gpa * s.gpa) - SUM(s.gpa) * SUM(s.gpa) / COUNT(*)) / (COUNT(*) - 1)
                            ) AS std_gpa_sample
                    FROM courses as c 
                    JOIN scores as s ON s.course_id = c.course_id
                    GROUP BY c.course_name
                    ORDER BY std_gpa_sample DESC
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["std_gpa_sample"]
            ) for data in department_row]
        except Exception as e:
            raise e
        
    def get_std_final_grade_by_course(self):
        try:
            query = text(
                """
                    SELECT
                        c.course_name,
                        SQRT(
                            (SUM(s.gpa * s.gpa) - SUM(s.gpa) * SUM(s.gpa) / COUNT(*)) / (COUNT(*) - 1)
                            ) AS std_final_grade_sample
                    FROM courses as c 
                    JOIN scores as s ON s.course_id = c.course_id
                    GROUP BY c.course_name
                    ORDER BY std_final_grade_sample DESC
                    LIMIT 10
                """
            )
            result = self.db.execute(query)
            department_row = result.mappings().all()
            return [AnalyticMetricDTO(
                column_categorical=data["course_name"],
                column_numerical=data["std_final_grade_sample"]
            ) for data in department_row]
        except Exception as e:
            raise e