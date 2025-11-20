import os
from src.config import DATA_DIR, load_pattern
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
DB_URL = os.getenv("DB_URL", f"sqlite:///{DATA_DIR}/student_score.db")
API_BASE = "https://manage-student-23ps.onrender.com"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
DETAIL_STUDENT_CONFIG = load_pattern("detail_student")
DOCX_CONFIG = load_pattern("docx")
ANALYTIC_CONFIG = load_pattern("analytic")
ERROR_CONFIG = load_pattern("error")
FORMAT_CONFIG = load_pattern("formats")
CONTENT_TYPE_CONFIG = load_pattern("content_type")
# INSIGHT_HISTORY_CONFIG = load_pattern("insight_history", folder_path=DATA_DIR)

class Role(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    
