import subprocess
from config.config import *

def run_backup(remote_file):
    dump_cmd = f"""
    mongodump \
      --uri="{MONGO_URI}" \
      --archive \
      --gzip \
    | ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "cat > {remote_file}"
    """
    subprocess.run(dump_cmd, shell=True, check=True)