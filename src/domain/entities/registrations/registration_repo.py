from abc import ABC, abstractmethod
from src.domain.entities.registrations.registration import Registration

class IsRegistrationRepo(ABC):
    @abstractmethod
    def get_by_id(self, registration_id:str) -> Registration | None:
        pass
    
    @abstractmethod
    def save(self, req_registration: Registration): 
        pass