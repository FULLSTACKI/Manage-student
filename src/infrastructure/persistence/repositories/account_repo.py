from sqlalchemy.orm import Session
from src.domain.entities.account import Account
from src.domain.repositories.account_repo import IsAccountRepo
from src.infrastructure.persistence.models import AccountModel

class AccountRepo(IsAccountRepo):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_username(self, username: str):
        acc = self.db.query(AccountModel).filter(AccountModel.username == username).first()
        if not acc:
            return None
        return Account(username=acc.username, password=acc.password, role=acc.role, student_id=acc.student_id)
