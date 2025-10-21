"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "n8n JSON Code Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./n8n_generator.db"
    
    # LLM Configuration
    DEFAULT_LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Local LLM (Ollama)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    
    # Learning System
    LEARNING_ENABLED: bool = True
    LEARNING_SCHEDULE_CRON: str = "0 0 * * 0"  # Every Sunday at midnight
    N8N_DOCS_URL: str = "https://docs.n8n.io"
    N8N_TEMPLATES_URL: str = "https://n8n.io/workflows"
    
    # GitHub
    GITHUB_TOKEN: str = ""
    GITHUB_SEARCH_QUERY: str = "n8n workflow"
    GITHUB_MIN_STARS: int = 10
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
