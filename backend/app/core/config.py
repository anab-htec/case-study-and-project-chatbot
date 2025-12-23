from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    WEAVIATE_HOST: str
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str  
    PROJECT_TECH_WEIGHT: float = 0.8
    PROJECT_SERVICE_WEIGHT: float = 0.2
    PROJECT_SCORE_THRESHOLD: float = 0.6
    CASE_STUDY_SCORE_THRESHOLD: float | None = None

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
    )

settings = Settings()