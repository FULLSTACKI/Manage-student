from abc import ABC, abstractmethod
from src.domain.entities.scores.score import Score

class IsScoreRepo(ABC):
    @abstractmethod
    def get_by_id(self, score_id:str) -> Score | None:
        pass
    
    @abstractmethod
    def save(self, req_score: Score): 
        pass