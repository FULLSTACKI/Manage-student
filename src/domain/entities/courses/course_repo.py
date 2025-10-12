from abc import ABC, abstractmethod
from src.domain.entities.courses.course import Course

class IsCourseRepo(ABC):
    @abstractmethod
    def get_by_id(self, course_id:str) -> Course | None:
        pass
    
    @abstractmethod
    def save(self, req_course: Course): 
        pass