from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """
    Читает .env-файлы.

    Использует `SecretStr`, чтобы работать с конфиденциальными данными,
    такими, как токен бота.
    """
    bot_token: SecretStr
    db_path: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
