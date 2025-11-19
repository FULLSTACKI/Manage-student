from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Các thư mục con quan trọng
SRC_DIR = BASE_DIR / "src"
DATA_DIR = SRC_DIR / "data"
UTIL_DIR = SRC_DIR / "utils"

# Các file cụ thể
CHART_DIR = DATA_DIR / "charts"
BACKUP_DIR = DATA_DIR / "backups"
SEED_DIR = DATA_DIR / "seed"
PATTERN_DIR = UTIL_DIR / "patterns"

DB_FILE_PATH = DATA_DIR / "student_score.db"
