from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_uri: str = "mysql+aiomysql://127.0.0.1:1487/db"
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    acces_token_expire_minutes: int = 30
    
settings = Settings()   