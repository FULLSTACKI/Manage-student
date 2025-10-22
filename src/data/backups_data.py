import os 
import shutil 
from datetime import datetime
from . import dir_path

def backup_csv(data_path=dir_path / "seed", backup_dir=dir_path/"backups/csv"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        destination = os.path.join(backup_dir, timestamp)
        os.makedirs(destination, exist_ok=True)
        shutil.copytree(data_path, destination, dirs_exist_ok=True)
        print(f"✅ CSV backup saved to {destination}")
    except Exception as e:
        raise e
    
    
def backup_database(backup_dir: str =dir_path/ "backups", database_path:str = "./student_score.db"):
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