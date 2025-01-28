"""Config Store"""
from json import dumps, loads
from sqlite3 import OperationalError
from typing import Any
from warnings import warn

from sqlite_database import Row, Table
from .database import config as _config, system_config as _system

IGNORED_MESSAGE = ("cannot commit - no transaction is active",)

def cast(data):
    """cast"""
    try:
        return loads(data)
    except Exception as exc:
        err = ValueError("There's a chance that data was not a native JSON type.")
        err.add_note(f"{type(exc).__name__}: {exc!s}")
        raise err from None

class _ConfigStore:
    """Config store"""
    def __init__(self, config_: Table = None):
        self._tb = config_ or _config
        # self._tb.exists()
        # try:
        #     if not self._tb.select_one():
        #         self._tb = init()[tbl_name]
        # except OperationalError:
        #     self._tb = init()[tbl_name]

    def __getitem__(self, name: str):
        result = self._tb.select_one({'name': name}, only="value")
        if isinstance(result, Row):
            raise KeyError(name)
        return cast(result)

    def __setitem__(self, name: str, value: Any):
        _check = self._tb.select_one({'name': name}, only='value')
        # print(_check)
        if isinstance(_check, Row):
            self._tb.insert({'name': name, 'value': dumps(value)})
            return
        try:
            self._tb.update_one({'name': name}, {'value': dumps(value)})
        except OperationalError as exc:
            if str(exc) not in IGNORED_MESSAGE:
                raise exc

        # self._tb.commit()

    def __delitem__(self, name: str):
        try:
            self._tb.delete_one({'name': name})
        except OperationalError as exc:
            warn(f"{exc}\n{'\n'.join(exc.__notes__)}")

    def __getattr__(self, name: str):
        # Fetch the attribute from _tb if it exists in the table
        if name == '_tb':  # For direct access to _tb attribute
            return object.__getattribute__(self, name)
        result = self._tb.select_one({"name": name}, only="value")
        if isinstance(result, Row):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return cast(result)

    def __setattr__(self, name: str, value: Any):
        if name == '_tb':  # Special case for setting _tb itself
            object.__setattr__(self, name, value)
        else:
            # Set the value in the table
            self[name] = value  # Delegate to __setitem__

    def __delattr__(self, name: str):
        if name == '_tb':
            raise AttributeError("Cannot delete '_tb' attribute")
        # Remove the corresponding entry from the table
        self.__delitem__(name)  # Delegate to __delitem__

    def __contains__(self, name: str):
        return bool(self._tb.select_one({'name': name}))

config = _ConfigStore()
system_config = _ConfigStore(_system)
