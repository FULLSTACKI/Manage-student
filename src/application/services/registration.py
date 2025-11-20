from src.domain.repositories.registration_repo import IsRegistrationRepo
from src.domain.entities.registration import Registration
from src.application.dtos.registration_dto import RegistrationResponse

class RegistrationManagement:
    def __init__(self, regis_repo: IsRegistrationRepo):
        self.regis_repo = regis_repo
        
    def register(self, student_id: str, course_id: str) -> RegistrationResponse:
        try:
            registration = Registration.add(student_id=student_id, course_id=course_id)
            if not registration:
                raise ValueError("Đăng kí thất bại")
            save_registration = self.regis_repo.save(student_id, course_id)
            if not save_registration:
                raise ValueError("Môn học đã đăng kí rồi! Đăng kí thất bại")
            return RegistrationResponse(
                success=True,
                message=f"Đăng kí mã học phần {course_id} thành công!"
            )
        except Exception as e:
            raise e