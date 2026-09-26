import os
from pathlib import Path
from dotenv import load_dotenv

# Path configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PAPERS_DIR = os.getenv("PAPERS_DIR", str(BASE_DIR / "data" / "papers"))
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", str(BASE_DIR / "data" / "vector_db"))

# Ensure data directories exist
Path(PAPERS_DIR).mkdir(parents=True, exist_ok=True)
Path(VECTOR_DB_DIR).mkdir(parents=True, exist_ok=True)
