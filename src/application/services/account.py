from src.domain.repositories import IsAccountRepo, IsSessionTokenRepo
from src.utils import ValidationError
from src.application.dtos.account_dto import *
import uuid
from datetime import datetime
import traceback
class AccountManagement:
    def __init__(self, account_repo: IsAccountRepo, token_repo: IsSessionTokenRepo):
        self.account_repo = account_repo
        self.token_repo = token_repo
        

    def create_token(self, username: str):
        """Tạo token mới khi đăng nhập"""
        try:
            token = str(uuid.uuid4())
            result = self.token_repo.create(username=username, token=token)
            return result.access_token
        except Exception as e:
            raise ValidationError("TOKEN_CREATION_FAILED", detail=str(e))

    def refresh_token(self, token: str):
        """Làm mới thời gian sống của token"""
        refreshed = self.token_repo.refresh_token(token)
        if not refreshed:
            raise ValidationError("TOKEN_NOT_FOUND", detail="Token không tồn tại hoặc hết hạn")
        return refreshed.token

    def get_current_user(self, token: str):
        try: 
            session = self.token_repo.get_by_token(token)

            if not session:
                raise ValidationError("INVALID_TOKEN", detail="Token không hợp lệ hoặc đã hết hạn")

            if session.expires_at < datetime.now():
                self.token_repo.delete(token)
                raise ValidationError("TOKEN_EXPIRED", detail="Phiên làm việc đã hết hạn")
            account = self.account_repo.get_by_username(session.username)
            if not account:
                self.token_repo.delete(token)
                raise ValidationError("NOT_FOUND", detail="Tài khoản không tồn tại.")

            return account
        except Exception as e:
            print("❌ ERROR RETRIEVING TOKEN ❌")
            traceback.print_exc()
            raise ValidationError("TOKEN_RETRIEVAL_FAILED", detail=str(e))


    def login(self, req: AccountLoginRequest) -> AccountResponse:
        account = self.account_repo.get_by_username(req.username)
        
        if not account:
            raise ValidationError("NOT_FOUND", detail="Tài khoản không tồn tại")
        
        if not account.verify_password(req_pass=req.password):
            raise ValidationError("INVALID_CREDENTIALS", detail="Sai mật khẩu")
        
        access_token = self.create_token(username=account.username)
        return AccountResponse(
            success=True,
            message="Đăng nhập thành công",
            access_token=access_token,
            student_id=account.student_id,
            role=account.role
        )