"""
Configuration management for Tim Urban Research Agent
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class that loads all environment variables"""
    
    # API Keys
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    YOUTUBE_API_KEY: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    SERP_API_KEY: Optional[str] = os.getenv("SERP_API_KEY")
    
    # MCP Configuration
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "tim-urban-research-agent")
    MCP_SERVER_VERSION: str = os.getenv("MCP_SERVER_VERSION", "0.1.0")
    
    # Agent Configuration
    MAX_RESEARCH_DEPTH: int = int(os.getenv("MAX_RESEARCH_DEPTH", "5"))
    MAX_YOUTUBE_VIDEOS: int = int(os.getenv("MAX_YOUTUBE_VIDEOS", "3"))
    MAX_WEB_ARTICLES: int = int(os.getenv("MAX_WEB_ARTICLES", "5"))
    BLOG_POST_MIN_LENGTH: int = int(os.getenv("BLOG_POST_MIN_LENGTH", "2000"))
    CARTOON_COUNT: int = int(os.getenv("CARTOON_COUNT", "3"))
    
    # Image generation settings
    DALLE_MODEL: str = os.getenv("DALLE_MODEL", "dall-e-3")
    DALLE_SIZE: str = os.getenv("DALLE_SIZE", "1024x1024")
    DALLE_QUALITY: str = os.getenv("DALLE_QUALITY", "standard")
    
    # Anthropic settings
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    @classmethod
    def get_all_vars(cls) -> dict:
        """Get all configuration variables as a dictionary"""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and not callable(getattr(cls, key))
        }
    
    @classmethod
    def validate_required_keys(cls) -> bool:
        """Validate that all required API keys are present"""
        required_keys = [
            cls.ANTHROPIC_API_KEY,
            cls.YOUTUBE_API_KEY,
            cls.SERP_API_KEY
        ]
        return all(key is not None for key in required_keys)

# Create a global config instance
config = Config()
