from abc import ABC, abstractmethod
from src.domain.entities import Student
from src.application.dtos import studentOut
from typing import List

class IsStudentRepo(ABC):
    @abstractmethod
    def get_by_id(self, student_id:str) -> studentOut | None:
        pass
    @abstractmethod
    def get_list_detail_student(self, col: List[str]) -> List[studentOut] | None:
        pass
    @abstractmethod
    def save(self, req_student: Student) -> studentOut: 
        pass
    @abstractmethod
    def update(self, req: Student) -> studentOut:
        pass
    @abstractmethod
    def deleted(self, student_id: str) -> studentOut:
        pass