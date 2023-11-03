from typing import Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    BOT_TOKEN: str
    EDITORS: Set[int] = set()

    class Config:
        case_sensitive = True
        env_file = ".env"
