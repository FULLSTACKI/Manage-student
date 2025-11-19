import os 
import shutil 
from datetime import datetime
from src.config import SEED_DIR, BACKUP_DIR, DB_FILE_PATH

def backup_csv(data_path=SEED_DIR, backup_dir=BACKUP_DIR/"csv"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        destination = os.path.join(backup_dir, timestamp)
        os.makedirs(destination, exist_ok=True)
        shutil.copytree(data_path, destination, dirs_exist_ok=True)
        print(f"✅ CSV backup saved to {destination}")
    except Exception as e:
        raise e
    
    
def backup_database(backup_dir=BACKUP_DIR, database_path=DB_FILE_PATH):
    try:
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = os.path.join(backup_dir, f"student_score_{timestamp}.db")
        shutil.copy2(database_path, backup_file)
        print(f"✅ Backup thành công: {backup_file}")
    except Exception as e:
        raise e
    
def _do_backup(snapshot_csv= False):
    backup_database()
    if snapshot_csv:
        backup_csv()