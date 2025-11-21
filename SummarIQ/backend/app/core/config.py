from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SummarIQ"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    
    # FalkorDB Settings
    FALKORDB_HOST: str = "localhost"
    FALKORDB_PORT: int = 6379
    FALKORDB_GRAPH_NAME: str = "summariq"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./summariq.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # LLM Settings - GROQ (fast inference)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"  # or "mixtral-8x7b-32768", "gemma2-9b-it"
    
    # OpenAI Settings (optional, for embeddings or fallback)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # LLM Provider selection
    LLM_PROVIDER: str = "groq"  # "groq" or "openai"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

