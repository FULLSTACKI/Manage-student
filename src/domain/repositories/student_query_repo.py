from abc import ABC, abstractmethod
from src.application.dtos import studentOut
from typing import List

class IsStudentQueryRepo(ABC):
    @abstractmethod
    def get_by_id(self, student_id:str) -> studentOut | None:
        pass
    @abstractmethod
    def get_list_detail_student(self, col: List[str]) -> List[studentOut] | None:
        pass