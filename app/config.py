import os
from pydantic import BaseSettings
from functools import lru_cache


def get_debug():
    return bool(os.getenv('DEBUG', False))


class Config(BaseSettings):
    BOT_URL: str = ""
    MONGO_HOST: str = '127.0.0.1'
    MONGO_PORT: int = 27017
    MONGO_USER: str = 'beard'
    MONGO_PASS: str = 'beard'
    DEBUG: bool = get_debug()

    class Config:
        env_file = ".dev.env" if get_debug() else ".env"


@lru_cache()
def get_config():
    return Config()
