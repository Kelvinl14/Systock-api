"""
Configuração centralizada da aplicação FastAPI.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    
    # API
    api_title: str = Field("Systock API", alias="API_TITLE")
    api_version: str = Field("1.0.0", alias="API_VERSION")
    debug: bool = Field(True, alias="DEBUG")
    
    # Logging
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()
