import subprocess
from config.config import *

def cleanup_old_backups():
    cmd = f'''
    ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} \
    "find {REMOTE_PATH} -type f -name '*.gz' -mtime +{RETENTION_DAYS - 1} -delete"
    '''
    subprocess.run(cmd, shell=True)