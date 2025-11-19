from abc import ABC, abstractmethod
from typing import List
from src.application.dtos import StudentHistoryResp

class IsStudentHistoryRepo(ABC):
    @abstractmethod
    def get_list_student_history(self) -> List[StudentHistoryResp]:
        pass