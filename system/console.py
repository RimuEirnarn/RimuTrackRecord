"""WebUI Command-line"""

from sys import executable
from shlex import split
from cmd import Cmd
from subprocess import run
from os import system as _system, chdir
from re import compile as re_compile, escape as re_escape, Pattern
from string import punctuation

from .config import ROOT
from .dependency import install_webui_dependency, clear_cache
from .configstore import _ConfigStore, system_config, config
from .database import config as config_table, system_config as system_config_table

chdir(ROOT)
undefined = object()
_INVALID_STR = punctuation.replace("_", "")
_re_valid = re_compile(f"[{re_escape(_INVALID_STR)}]+")


def matches(pattern: Pattern, value: str):
    """matches"""
    if len(pattern.findall(value)) == 0:
        return False
    return True


def check_name(varname):
    """check one to check if a string contains illegal character"""
    return matches(_re_valid, varname)


STATE: dict[str, _ConfigStore] = {"table": undefined}

MAP = {"true": True, "false": False, "null": None}


class WebUICMD(Cmd):
    """WebUI Command-line"""

    intro = "RimuTrackRecord Command-line"
    prompt = ">>> "

    def do_set_table(self, arg: str):
        """Set current table of edit. Unlocks set/delete/get/list/dump commands"""
        if not arg in ["system", "app"]:
            print("Not a valid table name. Expected system or app.")
            return
        if arg == "system":
            STATE["table"] = system_config
        if arg == "app":
            STATE["table"] = config
        return

    def do_unset_table(self, _):
        """Unset current table of edit"""
        STATE["table"] = undefined

    def do_update(self, _):
        """Update webui dependency"""
        install_webui_dependency()

    def do_reinstall(self, _):
        """Reinstall webui dependency"""
        install_webui_dependency(True)

    def do_clear_cache(self, _):
        """Clear caches"""
        clear_cache()

    def do_run(self, _):
        """Run main file as child process"""
        try:
            self.do_clear("")
            proc = run([executable, "main.py"], check=True)
            print("Child process returns: ", proc.returncode)
        except ChildProcessError as exc:
            print("Error with child process: ", str(exc))

    def do_clear(self, _):
        """Clear console"""
        _system("clear || cls")

    def do_set(self, joined_argv: str):
        """Set key-value name. Syntax is key=value.
        Be careful to put (") or (') if you want to capture whitespaced string."""
        if STATE["table"] is undefined:
            print("Table is undefined.")
            return
        argv = split(joined_argv)
        if len(argv) == 0:
            print("Syntax error: no sufficient arguments. Example: key='value'")
        base = argv[0]
        key, value = base.split("=", 1)
        real = value
        if check_name(key):
            print(f"Syntax error: {key!r}. Invalid character detected")
            return
        if value.isdecimal():
            real = float(value)
        if value.isnumeric():
            real = int(value)
        if value in MAP:
            real = MAP.get(value, value)
        STATE["table"][key] = real # pylint: disable=unsupported-assignment-operation

    def do_get(self, arg: str):
        """Get a value from current table."""
        if STATE["table"] is undefined:
            print("Table is undefined")
            return
        try:
            print(repr(STATE["table"][arg])) # pylint: disable=unsubscriptable-object
        except KeyError:
            pass

    def do_delete(self, arg: str):
        """Delete a value from current table."""
        if STATE["table"] is undefined:
            print("Table is undefined")
            return
        try:
            del STATE["table"][arg] # pylint: disable=unsupported-delete-operation
        except KeyError:
            pass

    def do_list(self, _):
        """Query all variables in current table"""
        if STATE["table"] is undefined:
            print("Table is undefined")
            return
        if STATE["table"] not in [system_config, config]:
            print("Neither does the table is valid table.")
            return
        table = system_config_table if STATE['table'] is system_config else config_table
        names = [row.name for row in table.select(only=("name",))]
        for index, name in enumerate(names, start=1):
            print(f"{index}. {name}")

    def do_dump(self, _):
        """Query all variables including its data in current table"""
        if STATE["table"] is undefined:
            print("Table is undefined")
            return
        if STATE["table"] not in [system_config, config]:
            print("Neither does the table is valid table.")
            return
        table = system_config_table if STATE['table'] is system_config else config_table
        data = {row.name: row.value for row in table.select()}
        for key, value in data.items():
            print(f"{key}={value}")

    def do_exit(self, _):
        """Exit"""
        return True
