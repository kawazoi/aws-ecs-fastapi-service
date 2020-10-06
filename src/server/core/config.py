import os
import logging
from dotenv import load_dotenv

from configparser import ConfigParser
from typing import Optional, Any


load_dotenv()


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
            NAME=self._fetch_from_env("API_NAME"), PORT=self._fetch_from_env("API_PORT")
        )

    @property
    def mongo(self) -> dict:
        return dict(
            MONGODB_URL=self._fetch_from_env("MONGODB_URL"), # deploying without docker-compose
            HOST=self._fetch_from_env("MONGO_HOST", "localhost"),
            PORT=self._fetch_from_env("MONGO_PORT", 27017),
            USER=self._fetch_from_env("MONGO_USER", "myuser"),
            PASSWORD=self._fetch_from_env("MONGO_PASSWORD", "mypassword123"),
            DB=self._fetch_from_env("MONGO_DB", "mydb"),
            MAX_CONNECTIONS_COUNT=self._fetch_from_env("MAX_CONNECTIONS_COUNT"),
            MIN_CONNECTIONS_COUNT=self._fetch_from_env("MIN_CONNECTIONS_COUNT"),
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
