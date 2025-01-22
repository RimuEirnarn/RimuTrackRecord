"""ConfigAPI"""
from typing import Any

from ..configstore import cast, config, _ConfigStore

undefined = object()

class ConfigAPI:
    """Configuration API"""
    def __init__(self, cfg: _ConfigStore = None):
        self._cfg = cfg or config

    def get(self, name: str, fallback: Any = undefined):
        """Get the value of a configuration"""
        try:
            return self._cfg[name]
        except KeyError:
            if fallback is undefined:
                raise
            return fallback

    def set(self, name: str, value):
        """Set the value of a configuration"""
        self._cfg[name] = value

    def delete(self, name: str):
        """Delete a configuration"""
        del self._cfg[name]

    def set_if_not_exists(self, name: str, value):
        """Set a configuration if it does not exist"""
        if name not in config:
            self._cfg[name] = value

    def config_dump(self):
        """Dump the configuration"""
        return self._cfg._tb.select() # pylint: disable=protected-access

    def as_object(self):
        """Return the configuration as a dict"""
        tb = self._cfg._tb # pylint: disable=protected-access
        return {a.name: cast(a.value) for a in tb.select()}
