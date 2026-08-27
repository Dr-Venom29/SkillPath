"""
Configuration handling for the backend.
It loads environment variables from a .env file located at the project root.
Only the required CognoDB credentials (and optional API settings) are exposed.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field

# Load .env from project root (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseSettings):
    COGNODB_URI: str = Field(..., env="COGNODB_URI")
    COGNODB_USERNAME: str = Field(..., env="COGNODB_USERNAME")
    COGNODB_PASSWORD: str = Field(..., env="COGNODB_PASSWORD")
    API_HOST: str = Field("127.0.0.1", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

# Instantiate a singleton settings object used throughout the app
settings = Settings()
