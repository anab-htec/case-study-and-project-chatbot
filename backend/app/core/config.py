from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    WEAVIATE_HOST: str   
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str  
    OPENAI_EMBED_MODEL: str
    OPENAI_CHAT_MODEL: str
    OPENAI_CONDENSE_MODEL: str
    OPENAI_PARSE_MODEL: str
    OPENAI_EVAL_MODEL: str
    OPENAI_SYNTHETIC_DATA_MODEL: str
    OPENAI_CHAT_TEMPERATURE: float
    OPENAI_PARSE_TEMPERATURE: float
    OPENAI_CONDENSE_TEMPERATURE: float
    OPENAI_EVAL_TEMPERATURE: float
    OPENAI_SYNTHETIC_DATA_TEMPERATURE: float
    OPENAI_PARSE_MAX_TOKENS: int
    OPENAI_CHAT_MAX_TOKENS: int
    OPENAI_CONDENSE_MAX_TOKENS: int
    OPENAI_EVAL_MAX_TOKENS: int
    OPENAI_SYNTHETIC_DATA_MAX_TOKENS: int
    OPENAI_CHAT_TOP_P: float      
    OPENAI_PARSE_TOP_P: float        
    OPENAI_CONDENSE_TOP_P: float      
    OPENAI_EVAL_TOP_P: float   
    OPENAI_SYNTHETIC_DATA_TOP_P: float
    OPENAI_MAX_RETRIES: int
    OPENAI_RETRY_INITIAL_BACKOFF_SECONDS: int
    OPENAI_RETRY_BACKOFF_MULTIPLIER: int 
    CLARIFICATION_MAX_ATTEMPTS: int = 2
    RETRIEVAL_TOP_K_CASE_STUDIES: int = 5
    RETRIEVAL_TOP_K_PROJECTS: int = 5
    PROJECT_TECH_WEIGHT: float = 0.8
    PROJECT_SERVICE_WEIGHT: float = 0.2
    PROJECT_SCORE_THRESHOLD: float = 0.6
    CASE_STUDY_SCORE_THRESHOLD: float | None = None

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
    )

settings = Settings()