from abc import ABC, abstractmethod
from src.domain.entities import Student

class IsStudentCommandRepo(ABC):
    @abstractmethod
    def find_by_id(self, student_id:str):
        pass
    @abstractmethod
    def save(self, req_student: Student) -> Student: 
        pass
    @abstractmethod
    def update(self, req: Student) -> Student:
        pass
    @abstractmethod
    def deleted(self, student_id: str) -> Student:
        pass