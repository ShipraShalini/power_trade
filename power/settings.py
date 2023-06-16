import os

ENV_LOCAL = "local"


class Settings:
    PROJECT_NAME: str = "power"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", ENV_LOCAL)
    SENTRY_DSN: str = os.getenv("SENTRY_DSN")
    DB_URL: str = os.getenv("DB_URL", "sqlite://db.sqlite3")


settings = Settings()

DB_MODULES = {"models": ["power.models"]}
