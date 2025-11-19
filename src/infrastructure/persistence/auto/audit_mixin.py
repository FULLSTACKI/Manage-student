from datetime import datetime
from sqlalchemy import event, inspect
import json

class AuditMixin:
    @staticmethod
    def register_audit(new_model, history_model):
        """Đăng ký sự kiện sao lưu dữ liệu khi update hoặc delete."""
        
        @event.listens_for(new_model, "before_update")
        def before_update(mapper, connection, target):
            state = inspect(target)
            changes = {}
            for attr in state.attrs:
                if attr.history.has_changes():
                    old_value = attr.history.deleted[0] if attr.history.deleted else None
                    new_value = attr.history.added[0] if attr.history.added else None
                    changes[attr.key] = {"old": old_value, "new": new_value}
            
            connection.execute(
                history_model.__table__.insert().values(
                        **{col.name: getattr(target, col.name) for col in mapper.columns},
                        user_email= "admin@gmail.com",
                        action= "UPDATE",
                        changed_at= datetime.utcnow(),
                        old_val= json.dumps({k: v["old"] for k, v in changes.items()}, default= str),
                        new_val= json.dumps({k: v["new"] for k, v in changes.items()}, default= str),
                )
            )
                    
        # @event.listens_for(new_model, "before_delete")
        # def before_delete(mapper, connection, target):
        #     connection.execute(
        #         history_model.__table__.insert().values(
        #                 **{col.name: getattr(target, col.name) for col in mapper.columns},
        #                 user_email= "admin@gmail.com",
        #                 action= "DELETE",
        #                 changed_at= datetime.utcnow(),
        #                 old_val= json.dumps({col.name: getattr(target, col.name) for col in mapper.columns}, default= str),
        #         )
        #     )