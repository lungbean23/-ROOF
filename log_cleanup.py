"""
Log Cleanup Utility for ┴ROOF Radio
Removes old broadcast logs, keeps only current session
"""

import shutil
from pathlib import Path
from datetime import datetime


def clean_logs(logs_dir="logs", keep_structure=True):
    """
    Clean all old logs from previous broadcasts
    
    Args:
        logs_dir: Path to logs directory
        keep_structure: If True, keeps directory structure but removes files
    
    Returns:
        Number of files removed
    """
    logs_path = Path(logs_dir)
    
    if not logs_path.exists():
        return 0
    
    files_removed = 0
    
    # Remove all JSON conversation files in root logs/
    for json_file in logs_path.glob("*.json"):
        json_file.unlink()
        files_removed += 1
        print(f"Removed old conversation: {json_file.name}")
    
    # Clean subdirectories
    subdirs = ["debug", "hosts/general", "interns/general"]
    
    for subdir in subdirs:
        subdir_path = logs_path / subdir
        
        if subdir_path.exists():
            for log_file in subdir_path.glob("*"):
                if log_file.is_file():
                    log_file.unlink()
                    files_removed += 1
    
    if files_removed > 0:
        print(f"\n🧹 Cleaned {files_removed} old log files")
        print(f"📻 Ready for fresh broadcast!\n")
    
    return files_removed


def create_current_session_marker(logs_dir="logs"):
    """
    Create a marker file for the current session
    Shows when the current broadcast started
    """
    logs_path = Path(logs_dir)
    logs_path.mkdir(exist_ok=True)
    
    marker_file = logs_path / "CURRENT_BROADCAST.txt"
    
    with open(marker_file, 'w') as f:
        f.write(f"Broadcast started: {datetime.now().isoformat()}\n")
        f.write(f"Logs in this directory are from the CURRENT session only.\n")
        f.write(f"Old logs are cleared at the start of each new broadcast.\n")
    
    return marker_file


if __name__ == "__main__":
    """Run cleanup when called directly"""
    print("\n┴ROOF Radio - Log Cleanup")
    print("=" * 50)
    clean_logs()
