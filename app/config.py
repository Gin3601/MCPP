from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    API_KEY: str = Field(..., env="API_KEY")
    API_URL: str = Field(..., env="API_URL")

    class Config:
        env_file = ".env"


# ⭐ 关键：在模块级创建实例
settings = Settings()
