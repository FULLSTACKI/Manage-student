from src.domain.repositories import IsStudentHistoryRepo
from ..dtos.student_history_dto import *
import traceback
from typing import List

class StudentHistoryManagement:
    def __init__(self, repo_student_history: IsStudentHistoryRepo):
        self.repo_student_history = repo_student_history
        
    def get_list_student_history(self) -> List[StudentHistoryResp]:
        try: 
            list_history_student = self.repo_student_history.get_list_student_history()
            return list_history_student 
        except Exception as e:
            print("Lỗi nằm ở đây!")
            traceback.print_exc()
            raise e