from sqlalchemy.orm import Session
from src.domain.repositories import IsOverviewKpiRepo
from src.domain.entities.dtos import OverviewKpi, OverviewTopStudent
from sqlalchemy import text
from typing import List

class OverviewRepo(IsOverviewKpiRepo):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_all_kpi(self) -> OverviewKpi:
        try:
            query = text("""
                SELECT 
                    (SELECT COUNT(student_id) FROM students) as total_student,
                    (SELECT COUNT(course_id) FROM courses) as total_course,
                    (SELECT AVG(gpa) FROM scores) as avg_gpa
            """)
            result = self.db_session.execute(query).mappings().first()
            return OverviewKpi(**result)
        except Exception as e:
            raise e  
        
    def get_top3_student(self) -> List[OverviewTopStudent]:
        try:
            query = text("""
                SELECT 
                    st.student_id,
                    st.student_name,
                    st.birthday,
                    sc.gpa,
                    d.department_name
                FROM students as st 
                JOIN scores as sc ON sc.student_id = st.student_id 
                JOIN departments as d ON d.department_id = st.department_id
                ORDER BY sc.gpa DESC 
                LIMIT 3 
            """)
            row_data = self.db_session.execute(query).mappings().all()
            return [OverviewTopStudent(**data) for data in row_data]
        except Exception as e:
            raise e  