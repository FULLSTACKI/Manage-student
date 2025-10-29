from abc import ABC, abstractmethod
from src.domain.entities import Student, StudentDetail
from typing import List

class IsStudentRepo(ABC):
    @abstractmethod
    def get_by_id(self, student_id:str) -> Student | None:
        pass
    @abstractmethod
    def get_list_detail_student(self, col: List[str]) -> List[Student] | None:
        pass
    @abstractmethod
    def save(self, req_student: Student): 
        pass
    @abstractmethod
    def update(self, req: Student) -> StudentDetail:
        pass
    @abstractmethod
    def deleted(self, student_id: str) -> StudentDetail:
        pass