import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import AnyHttpUrl

load_dotenv()


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    # SECURITY_BCRYPT_ROUNDS: int = 12
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0", "*"]

    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str = "PARSE SITES INDEXATION COLLATERAL"
    MONGO_COLLECT: str = "parse-sites-indexation-collateral"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Parse sites indexation collateral"
    WWW_DOMAIN = "/api/dms/parse-sites-indexation-collateral"
    DATABASE_URL = os.environ.get("DATABASE_URL")


class DevelopmentConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "DEV")  # type: ignore # ignored because we get it from env
    MONGO_URI: str = os.environ.get("MONGO_URI")  # type: ignore # ignored because we get it from env


class ProductionConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "PROD")  # type: ignore # ignored because we get it from env
    MONGO_URI: str = os.environ.get("MONGO_URI")  # type: ignore # ignored because we get it from env


class TestingConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "TEST")
    MONGO_URI: str = os.environ.get("MONGO_URI")  # type: ignore # ignored because we get it from env


class LocalConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "LOCAL")
    MONGO_URI: str = os.environ.get("MONGO_URI")  # type: ignore # ignored because we get it from env


class StagingConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "STAGING")
    MONGO_URI: str = os.environ.get("MONGO_URI")  # type: ignore # ignored because we get it from env


@lru_cache
def get_settings():
    config_cls_dict = {
        "DEV": DevelopmentConfig,
        "PROD": ProductionConfig,
        "TEST": TestingConfig,
        "LOCAL": LocalConfig,
        "STAGING": StagingConfig,
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "DEV")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
