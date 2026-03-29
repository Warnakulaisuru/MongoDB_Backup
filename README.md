📦 MongoDB Remote Backup Script

This Python script automates MongoDB backups by streaming a compressed dump directly to a remote server over SSH. It also handles backup rotation, keeping only the most recent backups.


🚀 Features
	•	🔄 Automated MongoDB backups using mongodump
	•	📡 Streams backup directly to a remote server via SSH (no local storage needed)
	•	🗜️ Compressed backups using gzip
	•	📁 Auto-creates remote backup directory if it doesn’t exist
	•	🧹 Keeps only the latest N backups (configurable)
	•	📊 Displays backup size after completion


🛠️ Requirements

Make sure the following are installed:
	•	Python 3.x
	•	MongoDB tools (mongodump)
	•	SSH access to remote server
	•	SSH key-based authentication (recommended)


⚙️ Configuration

Update the following variables in the script:

MONGO_URI = "mongodb://localhost:27017/"
REMOTE_USER = "USERNAME"
REMOTE_HOST = "BACKUP-VM-IP"
REMOTE_PORT = 22
REMOTE_PATH = "/path/to/backup/folder"
MAX_BACKUPS = 7

🔑 Notes
	•	Ensure SSH access works without password (use SSH keys).
	•	REMOTE_PATH must be writable by the remote user.


▶️ Usage

Run the script manually:

python backup.py


⏱️ Automating with Cron (Linux)

To run daily at 2 AM:

crontab -e

Add:

0 2 * * * /usr/bin/python3 /path/to/backup.py >> /var/log/mongo_backup.log 2>&1



📂 Backup Format

Backups are stored on the remote server as:

mongo_backup_YYYYMMDD_HHMMSS.gz

Example:

mongo_backup_20260329_021500.gz



🧹 Backup Retention

The script automatically deletes old backups:
	•	Keeps only the latest MAX_BACKUPS files
	•	Older files are removed automatically


⚠️ Error Handling
	•	Script exits if any step fails
	•	Displays error message in console/log
	•	Recommended to log output when using cron

🔐 Security Best Practices
	•	Use SSH key authentication instead of passwords
	•	Restrict SSH access to trusted IPs
	•	Ensure backup directory permissions are secure


📌 Example Workflow
	1.	Script connects to remote server
	2.	Ensures backup directory exists
	3.	Runs mongodump locally
	4.	Streams compressed data over SSH
	5.	Saves .gz file remotely
	6.	Deletes old backups
