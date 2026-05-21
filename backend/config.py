import os
from dotenv import load_dotenv
from typing import Optional


# Load environment variables
load_dotenv()

class Config:
    # Qdrant configuration
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Database configuration
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    # LLM configuration
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")  # Default to Gemini
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))

    # Provider-specific models
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # Embedding configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Application settings
    APP_NAME: str = "Physical AI Book API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # RAG settings
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "3"))  # Number of chunks to retrieve
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))  # Size of text chunks
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))  # Overlap between chunks

    # Rate limiting configurations
    CHAT_RATE_LIMIT: str = os.getenv("CHAT_RATE_LIMIT", "10/minute")
    HEALTH_RATE_LIMIT: str = os.getenv("HEALTH_RATE_LIMIT", "100/minute")
    ROOT_RATE_LIMIT: str = os.getenv("ROOT_RATE_LIMIT", "100/minute")
    INGEST_RATE_LIMIT: str = os.getenv("INGEST_RATE_LIMIT", "5/hour")
    MONITORING_RATE_LIMIT: str = os.getenv("MONITORING_RATE_LIMIT", "10/minute")

# Validate required environment variables
def validate_config():
    required_vars = ["QDRANT_URL", "DATABASE_URL", "LLM_API_KEY"]
    missing_vars = []

    for var in required_vars:
        if not getattr(Config, var):
            missing_vars.append(var)

    if missing_vars:
        # In production/deployment, we log a warning instead of crashing.
        # This allows the app to serve the frontend textbook even if the AI backend isn't ready.
        print(f"CRITICAL WARNING: Missing required environment variables: {', '.join(missing_vars)}")
        print("The AI Chatbot functionality will be unavailable until these are set in the Space settings.")

# Validate configuration on import
validate_config()

config = Config()