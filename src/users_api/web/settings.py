from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    # debug: bool = True
    postgres_host: str | None = None
    postgres_port: int | None = None
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()
