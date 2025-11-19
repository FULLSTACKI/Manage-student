from src.application.dtos.token_dto import TokenDTO
from src.infrastructure.persistence.models.token_model import SessionTokenModel

class TokenMapper:
    @staticmethod
    def to_dto(token_model: SessionTokenModel) -> TokenDTO:
        return TokenDTO(
            access_token=token_model.token,
            expires_at=token_model.expires_at,
            username=token_model.username,
            created_at=token_model.created_at
        )