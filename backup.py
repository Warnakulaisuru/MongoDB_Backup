import subprocess
import datetime
import sys
import os

# CONFIG
MONGO_URI = "mongodb://localhost:27017/"
REMOTE_USER = "USERNAME"
REMOTE_HOST = "BACKUP-VM-IP"
REMOTE_PORT = 22 # SSH port, change if not default
REMOTE_PATH = "location/of/backup/folder"  # e.g., /home/username/backups
MAX_BACKUPS = 7  # keep only last 7 backups

# Generate timestamped backup filename
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
remote_file = f"{REMOTE_PATH}/mongo_backup_{timestamp}.gz"

def run_backup():
    try:
        # 1. Ensure remote backup folder exists
        mkdir_cmd = f'ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "mkdir -p {REMOTE_PATH}"'
        subprocess.run(mkdir_cmd, shell=True, check=True)

        # 2. Run MongoDB backup and stream to remote server
        dump_cmd = f"""
        mongodump \
          --uri="{MONGO_URI}" \
          --archive \
          --gzip \
        | ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "cat > {remote_file}"
        """
        subprocess.run(dump_cmd, shell=True, check=True)
        print(f"[SUCCESS] Backup saved to {REMOTE_HOST}:{remote_file}")

        # 3. Check size of backup file on remote
        size_cmd = f'ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "du -h {remote_file} | cut -f1"'
        size = subprocess.check_output(size_cmd, shell=True).decode().strip()
        print(f"Backup size: {size}")

        # 4. Cleanup old backups (keep only last MAX_BACKUPS)
        cleanup_cmd = f'ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "ls -1t {REMOTE_PATH}/*.gz | tail -n +{MAX_BACKUPS+1} | xargs -r rm -f"'
        subprocess.run(cleanup_cmd, shell=True)
        print(f"[INFO] Old backups cleaned, keeping last {MAX_BACKUPS} files.")

    except subprocess.CalledProcessError as e:
        print("[ERROR] Backup failed!", e)
        sys.exit(1)

if __name__ == "__main__":
    print("Starting MongoDB backup...")
    run_backup()
    print("Backup completed!")