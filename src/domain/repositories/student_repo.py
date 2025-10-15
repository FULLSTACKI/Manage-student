from abc import ABC, abstractmethod
from src.domain.entities.students.student import Student 

class IsStudentRepo(ABC):
    @abstractmethod
    def get_by_id(self, student_id:str) -> Student | None:
        pass
    
    @abstractmethod
    def save(self, req_student: Student): 
        pass