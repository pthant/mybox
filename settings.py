from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    R2_ACCOUNT_ID: str
    R2_APP_KEY: str
    R2_APP_SECRET: str
    R2_BUCKET: str
    DB_APP_KEY: str
    DB_APP_SECRET: str
    DB_INIT_ACCESS_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")
