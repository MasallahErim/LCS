# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    kafka_bootstrap: str = "kafka:9092"
    redis_url: str      = "redis://redis:6379/0"
    postgres_url: str   = "postgresql://comment_user:secretpass@postgres:5432/commentsdb"
    grpc_host: str      = "sentiment"
    grpc_port: int      = 50051
    api_host: str       = "0.0.0.0"
    api_port: int       = 8000


    class Config:
        env_file = ".env"

settings = Settings()
