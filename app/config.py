import os
from pydantic import BaseSettings
from functools import lru_cache


# TODO: брать конфиг из файла в зависимости от переменной dev
# TODO: исправить временные значения на стандартные для продакшн сборки
class Config(BaseSettings):
    SCOREBOARD: str = os.getenv('SCOREBOARD', 'http://127.0.0.1:8090')
    TEAM: str = os.getenv('TEAM', 'Red Cadets')
    TYPE: str = os.getenv('TYPE', 'forcad')
    BOT_URL: str = os.getenv('BOT_URL', 'https://bot.example.com/key')
    MONGO_HOST: str = os.getenv('MONGO_HOST', '127.0.0.1')
    MONGO_PORT: int = int(os.getenv('MONGO_PORT', '27017'))
    MONGO_USER: str = os.getenv('MONGO_USER', 'beard')
    MONGO_PASS: str = os.getenv('MONGO_PASS', 'beard')
    ROUND_TIME: int = int(os.getenv('ROUND_TIME', '120'))
    EXTEND_ROUND: int = int(os.getenv('EXTEND_ROUND', '50'))
    DEBUG: bool = bool(os.getenv('DEBUG', 'true'))


@lru_cache()
def get_config():
    return Config()
