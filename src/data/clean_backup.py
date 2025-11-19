import os
from src.config import BACKUP_DIR

def cleanup_by_file_count(backup_dir=BACKUP_DIR, max_files=10):
    
    if not os.path.exists(backup_dir):
        return

    files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.endswith(".db")]
    files.sort(key=os.path.getmtime, reverse=True)  # Sắp xếp từ mới → cũ

    if len(files) > max_files:
        for old_file in files[max_files:]:
            os.remove(old_file)

        print(f"🧹 Dọn dẹp backup: giữ lại {max_files} file mới nhất, đã xóa {len(files) - max_files} file cũ.")
