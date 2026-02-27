from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    ENV: str = "development"
    DATABASE_URL: str = "postgressql://user:pass@localhost:5432/app"
    REDDIS_URL: str = "redis://localhost:6379"
    ALLOWED_ORIGINS: str = "*"

settings = Settings()