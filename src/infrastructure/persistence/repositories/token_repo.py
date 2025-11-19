from datetime import datetime, timedelta
from src.infrastructure.persistence.models import SessionTokenModel
from src.domain.repositories.token_repo import IsSessionTokenRepo
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.infrastructure.persistence.mappers import TokenMapper

class SessionTokenRepo(IsSessionTokenRepo):
    def __init__(self, db_session: Session):
        self.db = db_session 

    def create(self, username: str, token: str, expire_minutes: int = 3600) -> SessionTokenModel:
        expires_at = datetime.now() + timedelta(minutes=expire_minutes)
        session = SessionTokenModel(
            token=token,
            username=username,
            expires_at=expires_at
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return TokenMapper.to_dto(session)

    def get_by_token(self, token: str) -> SessionTokenModel | None:
        try:
            result = self.db.query(SessionTokenModel).filter(SessionTokenModel.token == token).first()
            if result:
                return TokenMapper.to_dto(result)
        except IntegrityError as e:
            self.db.rollback()
            raise e

    def delete(self, token: str):
        session = self.get_by_token(token)
        if session:
            self.db.delete(session)
            self.db.commit()

    def refresh_token(self, token: str, extra_minutes: int = 120):
        session = self.db.query(SessionTokenModel).filter(SessionTokenModel.token == token).first()
        if not session:
            return None
        session.expires_at = datetime.utcnow() + timedelta(minutes=extra_minutes)
        self.db_session.commit()
        return TokenMapper.to_dto(session)
    
