from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()
