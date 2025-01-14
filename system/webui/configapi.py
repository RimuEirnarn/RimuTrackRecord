"""ConfigAPI"""
from typing import Any
from ..configstore import config

undefined = object()

class ConfigAPI:
    """Configuration API"""
    def __init__(self):
        pass

    def get(self, name: str, fallback: Any = undefined):
        """Get the value of a configuration"""
        try:
            return config[name]
        except KeyError:
            if fallback is undefined:
                raise
            return fallback

    def set(self, name: str, value):
        """Set the value of a configuration"""
        config[name] = value

    def delete(self, name: str):
        """Delete a configuration"""
        del config[name]

    def set_if_not_exists(self, name: str, value):
        """Set a configuration if it does not exist"""
        if name not in config:
            config[name] = value

    def config_dump(self):
        """Dump the configuration"""
        return config._tb.select() # pylint: disable=protected-access
