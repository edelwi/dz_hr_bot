from functools import lru_cache
from app.config_base import Settings


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
