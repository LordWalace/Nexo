from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Nexo API"
    APP_SLUG: str = "nexo"
    APP_ENV: str = "development"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None

    STORAGE_ENDPOINT: str
    STORAGE_ACCESS_KEY: str
    STORAGE_SECRET_KEY: str
    STORAGE_BUCKET: str

    MAX_FILE_SIZE_MB: int = 10
    MAX_USER_STORAGE_MB: int = 100

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"), env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()  # type: ignore
