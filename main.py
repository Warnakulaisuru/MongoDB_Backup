import datetime
import sys

from core.backup import run_backup
from core.cleanup import cleanup_old_backups
from core.ssh import ensure_remote_dir, get_remote_file_size
from utils.logger import get_logger
from config.config import REMOTE_PATH, REMOTE_HOST

logger = get_logger()

def main():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        remote_file = f"{REMOTE_PATH}/mongo_backup_{timestamp}.gz"

        logger.info("Starting backup...")

        ensure_remote_dir()
        run_backup(remote_file)

        size = get_remote_file_size(remote_file)
        logger.info(f"Backup saved: {REMOTE_HOST}:{remote_file} | Size: {size}")

        cleanup_old_backups()
        logger.info("Old backups cleaned")

        logger.info("Backup completed successfully")

    except Exception as e:
        logger.error(f"Backup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()