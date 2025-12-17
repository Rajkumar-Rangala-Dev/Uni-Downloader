import os
from dotenv import load_dotenv

load_dotenv()

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 200))
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", 600))
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp")
