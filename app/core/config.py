from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import Field

class Settings(BaseSettings):
    # ---------- Application ----------
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")

    # ---------- Database ----------
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ---------- Security / JWT ----------
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ---------- Redis ----------
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")

    # ---------- Rate Limiting ----------
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_PERIOD_SECONDS: int = Field(default=60, env="RATE_LIMIT_PERIOD_SECONDS")

    # ---------- Optional Email ----------
    EMAIL_HOST: str | None = Field(default=None, env="EMAIL_HOST")
    EMAIL_PORT: int | None = Field(default=None, env="EMAIL_PORT")
    EMAIL_USER: str | None = Field(default=None, env="EMAIL_USER")
    EMAIL_PASSWORD: str | None = Field(default=None, env="EMAIL_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
