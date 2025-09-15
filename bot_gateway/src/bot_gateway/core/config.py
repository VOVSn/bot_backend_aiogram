from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_HOST: str
    TELEGRAM_SECRET_TOKEN: str = "super_secret_token"
    CONSUL_HOST: str = "localhost"
    CONSUL_PORT: int = 8500

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()