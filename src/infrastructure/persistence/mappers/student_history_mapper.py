from src.infrastructure.persistence.models import StudentHistoryModel
from src.application.dtos import StudentHistoryResp, studentOut

class StudentHistoryMapper:
    @staticmethod
    def to_history_detail(model: StudentHistoryModel) -> StudentHistoryResp:
        history_model = model[0] 
        dept_name = model[1]
        return StudentHistoryResp(
            user_email=history_model.user_email,
            action=history_model.action,
            change_at=history_model.changed_at,
            old_val=history_model.old_val,
            new_val=history_model.new_val,
            detail=studentOut(
                student_id=history_model.student_id,
                student_name=history_model.student_name,
                email=history_model.email,
                age=history_model.age,
                birthday=history_model.birthday,
                sex=history_model.sex,
                departments=dept_name,
                birthplace=history_model.birthplace,
                address=history_model.address,
                phone=history_model.phone,
                ethnicity=history_model.ethnicity,
                religion=history_model.religion,
                id_card=history_model.id_card,
                issue_date=history_model.issue_date,
                issue_place=history_model.issue_place
            )
        )