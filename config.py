import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = INSTANCE_DIR / "workshop.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False