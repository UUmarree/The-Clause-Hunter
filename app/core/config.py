from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Metadata
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str = "/api/v1"

    # Worker & Database Configuration
    REDIS_URL: str
    
    # ML Parameters
    MODEL_CONFIDENCE_THRESHOLD: float

    # Pydantic V2 config to read from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate the settings object so we can import it anywhere
settings = Settings()