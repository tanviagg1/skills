import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str = os.environ.get("GROQ_API_KEY", "")
    github_token: str = os.environ.get("GITHUB_TOKEN", "")
    linear_api_key: str = os.environ.get("LINEAR_API_KEY", "")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
