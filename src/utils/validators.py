import json
import re
from typing import Optional
from pathlib import Path

from src.models.schemas import UploadScoreRequest, UploadStudentRequest, UploadCourseRequest

FORMATS_PATH = Path(__file__).parent / "formats.json"
_patterns = {}
if FORMATS_PATH.exists():
    try:
        _patterns = json.loads(FORMATS_PATH.read_text(encoding="utf-8"))
    except Exception:
        _patterns = {}

_id_re = re.compile(_patterns.get("student_id", "^[A-Za-z0-9_-]+$"))
_score_re = re.compile(_patterns.get("score", r"^\d{1,2}(\.\d+)?$"))
_name_re = re.compile(_patterns.get("name", r"^[A-Za-zÀ-ÖØ-öø-ÿ ']{10,25}$"))
_email_re = re.compile(_patterns.get("email", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"))
_date_re = re.compile(_patterns.get("date", r"^\d{4}-\d{2}-\d{2}$"))
_sex_re = re.compile(_patterns.get("sex", r"^(M|F|Unknown)$"))      

def validate_id(student_id: str) -> bool:
    if not isinstance(student_id, str):
        return False
    return bool(_id_re.match(student_id))

def validate_score(value) -> bool:
    try:
        # allow numeric input or string matching pattern
        if isinstance(value, (int, float)):
            v = float(value)
            return 0.0 <= v <= 10.0
        if isinstance(value, str):
            if not _score_re.match(value):
                return False
            v = float(value)
            return 0.0 <= v <= 10.0
    except Exception:
        return False
    return False

def validate_name(name: str) -> bool:
    if not isinstance(name, str):
        return False
    return bool(_name_re.match(name))

def validate_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    return bool(_email_re.match(email))

def validate_date(birthday: str) -> bool:
    if not isinstance(birthday, str):
        return False
    return bool(_date_re.match(birthday))

def validate_sex(sex: str) -> bool:
    if not isinstance(sex, str):
        return False
    return bool(_sex_re.match(sex))

def validate_credits(credits: int) -> bool:
    if not isinstance(credits, int):
        return False
    return 1 <= credits <= 5

def validate_upload_student_request(req: UploadStudentRequest) -> Optional[str]:
    if not validate_id(req.id):
        return "invalid id"
    if not validate_name(req.name):
        return "invalid name"
    if not validate_email(req.email):
        return "invalid email"
    if not validate_date(req.birthday):
        return "invalid birthday"
    if not validate_sex(req.sex):
        return "invalid sex"
    return None

def validate_upload_score_request(req: UploadScoreRequest) -> Optional[str]:
    if not validate_id(req.student_id):
        return "invalid student_id"
    if not validate_id(req.course_id):
        return "invalid course_id"
    if not validate_score(req.coursework_grade):
        return "invalid coursework_grade"
    if not validate_score(req.midterm_grade):
        return "invalid midterm_grade"
    if not validate_score(req.final_grade):
        return "invalid final_grade"
    if not validate_score(req.gpa):
        return "invalid gpa"
    return None

def validate_upload_course_request(req: UploadCourseRequest) -> Optional[str]:
    if not validate_id(req.id):
        return "invalid id"
    if not validate_name(req.name):
        return "invalid name"
    if not validate_date(req.start_course):
        return "invalid start_date"
    if not validate_credits(req.credits):
        return "invalid credits"
    return None

__all__ = [
    "validate_student_id",
    "validate_course_id",
    "validate_score",
    "validate_upload_score_request",
    "validate_registration_ids",
    "validate_upload_student_request",
]


