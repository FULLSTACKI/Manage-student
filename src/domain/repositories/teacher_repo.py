from abc import ABC, abstractmethod
from src.domain.entities import Teacher
from typing import List

class IsTeacherRepo(ABC):
    @abstractmethod
    def get_by_id(self, teacher_id: str) -> Teacher:
        pass 
    
    @abstractmethod
    def get_all(self) -> List[Teacher]:
        pass 
    
    @abstractmethod
    def save(self, teacher_id: str) -> Teacher:
        pass
     