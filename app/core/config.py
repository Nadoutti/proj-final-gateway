from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    INGRESSOS_SERVICE_URL: str
    USUARIOS_SERVICE_URL: str
    EVENTOS_SERVICE_URL: str

    APP_PORT: int = 8080

    class Config:
        env_file = ".env"


settings = Settings()
