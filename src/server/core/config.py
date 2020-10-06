""" src.server.core.config.ConfigManager centralizes environment variables """

import logging
import os
from configparser import ConfigParser
from typing import Any, Optional

import uvicorn
from dotenv import load_dotenv

load_dotenv()

LOG_FORMAT = ("%(asctime)s - %(levelname)s - %(name)s - %(message)s",)


class ConfigManager:
    """
    Use this class instead of making direct reference to env
    to centralize constants names and such.
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
                        "%s not found as env var but assumed a default value %s",
                        varname,
                        default,
                    )
        return value
