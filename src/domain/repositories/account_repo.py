from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.account import Account

class IsAccountRepo(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Account]:
        pass
