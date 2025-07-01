from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Info
    PROJECT_NAME: str = "FastAPI Industrial App"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Industrial grade FastAPI application with separated routes and services"
    API_V1_STR: str = "/api/v1"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Cassandra Configuration
    CASSANDRA_HOST: str = "172.31.4.229"
    CASSANDRA_USERNAME: str = "cassandra"
    CASSANDRA_PASSWORD: str = "cassandra"
    CASSANDRA_KEYSPACE: str = "myapp"
    CASSANDRA_PORT: int = 9042
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # External Services
    EXTERNAL_API_URL: Optional[str] = None
    EXTERNAL_API_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


# Create settings instance
settings = Settings() 