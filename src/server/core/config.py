from typing import Optional, Any
import logging
import os
import uvicorn

from configparser import ConfigParser
from databases import DatabaseURL
from dotenv import load_dotenv


load_dotenv()

LOG_FORMAT = ("%(asctime)s - %(levelname)s - %(name)s - %(message)s",)


class ConfigManager:
    """
    Use this class instead of making direct reference to env
    To centralize constants names and such.
    """

    def __init__(self, echo=False):
        self.echo = echo
        self.config = ConfigParser()

    @property
    def api(self) -> dict:
        return dict(
            NAME=self._fetch_from_env("API_NAME"),
            PORT=int(self._fetch_from_env("API_PORT")),
        )

    @property
    def uvicorn(self) -> dict:
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["formatters"]["access"]["fmt"] = LOG_FORMAT
        return dict(
            LOG_CONFIG=log_config,
            LOG_LEVEL=self._fetch_from_env("UVICORN_LOG_LEVEL", "info"),
            RELOAD=bool(int(self._fetch_from_env("UVICORN_RELOAD", 0))),
        )

    @property
    def mongo(self) -> dict:
        MONGODB_URL = self._fetch_from_env(
            "MONGODB_URL"
        )  # deploying without docker-compose

        if not MONGODB_URL:
            HOST = self._fetch_from_env("MONGO_HOST", "localhost")
            PORT = self._fetch_from_env("MONGO_PORT", 27017)
            USER = self._fetch_from_env("MONGO_USER", "admin")
            PASSWORD = self._fetch_from_env("MONGO_PASSWORD", "admin123")
            DB = self._fetch_from_env("MONGO_DB", "fastapi")

            MONGODB_URL = DatabaseURL(f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
        else:
            MONGODB_URL = DatabaseURL(MONGODB_URL)

        return dict(
            MONGODB_URL=MONGODB_URL,
            MAX_CONNECTIONS_COUNT=self._fetch_from_env("MAX_CONNECTIONS_COUNT"),
            MIN_CONNECTIONS_COUNT=self._fetch_from_env("MIN_CONNECTIONS_COUNT"),
        )

    @property
    def log(self) -> dict:
        return dict(
            LOG_FORMAT="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            LOG_LEVEL=self._fetch_from_env("LOG_LEVEL"),
        )

    def _fetch_from_env(self, varname: str = "", default: Any = None) -> Optional[str]:
        """
        Tries to fetch a variable from the conf file, falls back to env var.

        :param varname: Name of the env var to fallback to
        :param default: If the value is not set, return default instead.
        :return The value, if found, otherwise default.
        """

        value = os.environ.get(varname, None)
        if not value:
            if default is not None:
                value = default
                if self.echo:
                    logging.warning(
                        "{} not found as environment var but assumed a default value {}".format(
                            varname, default
                        )
                    )
        return value
