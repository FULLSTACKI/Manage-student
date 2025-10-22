from abc import ABC, abstractmethod
from src.domain.entities.score import Score

class IsScoreRepo(ABC):
    @abstractmethod
    def get_by_id(self, score_id:str) -> Score | None:
        pass
    
    # @abstractmethod
    # def get_avg_gpa_all(self) -> float:
    #     pass
    
    @abstractmethod
    def save(self, req_score: Score) -> Score | None: 
        pass