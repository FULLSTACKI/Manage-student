from src.infrastructure.persistence.models import SessionTokenModel
from abc import ABC, abstractmethod

class IsSessionTokenRepo(ABC):
    @abstractmethod
    def create(self, username: str, token: str, expire_minutes: int) -> SessionTokenModel:
        pass
    @abstractmethod
    def get_by_token(self, token: str) -> SessionTokenModel | None:
        pass
    @abstractmethod
    def delete(self, token: str):
        pass
    @abstractmethod
    def refresh_token(self):
        pass
    
