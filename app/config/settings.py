
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    # Groq configuration
    GROQ_API_KEY: str
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    # Gemini configuration
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.8-flash"

    # Shared generation settings
    TEMPERATURE: float = Field(default=0.2, ge=0, le=1)
    MAX_TOKENS: int = Field(default=4096, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
