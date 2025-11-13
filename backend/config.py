"""
Backend Configuration Management
"""
from typing import List
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """Application settings from environment variables"""

    def __init__(self):
        # Environment
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "true").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # API Keys
        self.together_api_key = os.getenv("TOGETHER_API_KEY", "")
        self.cohere_api_key = os.getenv("COHERE_API_KEY", "")
        self.huggingface_api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")

        # Database
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./brand_identity.db")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

        # LLM Configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "ollama")  # ollama, together, cohere
        self.llm_model = os.getenv("LLM_MODEL", "mistral")
        self.llm_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1024"))
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        
        # Ollama Configuration (for local LLM)
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Security
        self.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

        # Training
        self.training_data_path = os.getenv("TRAINING_DATA_PATH", "./data/training")
        self.models_path = os.getenv("MODELS_PATH", "./models")
        self.batch_size = int(os.getenv("BATCH_SIZE", "8"))
        self.epochs = int(os.getenv("EPOCHS", "3"))
        self.learning_rate = float(os.getenv("LEARNING_RATE", "2e-5"))

        # CORS - Allow all localhost/127.0.0.1 ports for development
        cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:3001,http://127.0.0.1:3002,http://127.0.0.1:3003,http://127.0.0.1:8000")
        self.cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]


settings = Settings()

