import os

# Use absolute path from project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend directory
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
LATEST_RESUME_PATH = os.path.join(UPLOAD_DIR, "resume.pdf")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)