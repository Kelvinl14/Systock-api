"""
Configuração centralizada da aplicação FastAPI.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # Database
    database_url: str
    
    # API
    api_title: str = "Systock API"
    api_version: str = "1.0.0"
    debug: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
