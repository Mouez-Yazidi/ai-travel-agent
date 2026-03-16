"""
Configuration and environment variables.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# API keys (support multiple env var names for flexibility)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = (
    os.getenv("OPEN_WEATHER_API_KEY") or os.getenv("OPENWEATHER_API_KEY")
)


def require_groq_key() -> str:
    """Return GROQ API key or raise if missing."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Add it to .env or your environment."
        )
    return GROQ_API_KEY
