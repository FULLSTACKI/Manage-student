from src.infrastructure.persistence.auto.audit_mixin import AuditMixin 
from sqlalchemy import event
from src.infrastructure.persistence.models import StudentHistoryModel, StudentModel

def set_up_events():
    AuditMixin.register_audit(StudentModel, StudentHistoryModel)
    print("✅ Đã đăng ký thành công các Domain Events (Audit).")