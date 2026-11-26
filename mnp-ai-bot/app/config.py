import os
from pathlib import Path
from dotenv import load_dotenv

# Find .env relative to this file
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
load_dotenv()

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/mnp_bot_db"
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "prod-insecure-change-in-production-key-32chars")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip('"').strip("'")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
