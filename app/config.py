from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str 
    access_token_expiration: str

    class Config:
        env_file = ".env"  # Specify the .env file to load

settings = Settings()