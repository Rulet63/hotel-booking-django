from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Django
    secret_key: str = Field(default="django-insecure-dev-key", env="SECRET_KEY")
    debug: bool = Field(default=True, env="DEBUG")
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")
    
    # Database
    database_url: Optional[PostgresDsn] = Field(
        default="postgresql://hotel_user:hotel_password@localhost:5432/hotel_db",
        env="DATABASE_URL"
    )
    
    # Docker
    docker_container: bool = Field(default=False, env="DOCKER_CONTAINER")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        
        # Build from individual components
        return PostgresDsn.build(
            scheme="postgresql",
            username=os.getenv("POSTGRES_USER", "hotel_user"),
            password=os.getenv("POSTGRES_PASSWORD", "hotel_password"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            path=f"/{os.getenv('POSTGRES_DB', 'hotel_db')}",
        )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
