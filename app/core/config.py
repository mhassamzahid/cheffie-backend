from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_DB_URL: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_FROM_NUMBER: str

    model_config = SettingsConfigDict(
        env_file=".env",        # Used locally
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()