import subprocess
from config.config import *

def ensure_remote_dir():
    cmd = f'ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "mkdir -p {REMOTE_PATH}"'
    subprocess.run(cmd, shell=True, check=True)

def get_remote_file_size(remote_file):
    cmd = f'ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} "du -h {remote_file} | cut -f1"'
    return subprocess.check_output(cmd, shell=True).decode().strip()