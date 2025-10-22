from abc import ABC, abstractmethod
from src.domain.entities.student import Student 
from typing import List

class IsStudentRepo(ABC):
    @abstractmethod
    def get_by_id(self, student_id:str) -> Student | None:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Student] | None:
        pass
    
    @abstractmethod
    def save(self, req_student: Student): 
        pass