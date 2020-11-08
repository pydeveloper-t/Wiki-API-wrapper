from pydantic import BaseSettings,  RedisDsn, PostgresDsn

class Settings(BaseSettings):
    use_db: str = 'postgresql'
    redis_dsn: RedisDsn = ''
    postgres_dsn: PostgresDsn = ''

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()