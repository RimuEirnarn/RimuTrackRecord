"""main"""

from os import remove
try:
    remove("temp/profile/config.db")
except FileNotFoundError:
    pass

from argh import ArghParser, set_default_command
from dotenv import load_dotenv
import webview
import system.log
import system.database
import system.webui.api
import system.config
import system.configstore
import system.dependency

# system.log.info("Starting RimuTrackRecord")
load_dotenv()
# system.database.init()

def clear():
    """Clear all webui dependency caches"""
    system.dependency.clear_cache()

def delete_config():
    """Delete config database"""
    remove(system.config.CONFIG_DIR / "config.db")

def update(force: bool = False):
    """Update webui dependency if necessary"""
    system.dependency.install_webui_dependency(force)

def seed():
    """Seed the database"""
    import system.fake # pylint: disable=import-outside-toplevel,redefined-outer-name
    system.fake.seeder()

def install():
    """Install"""
    if (system.config.CONFIG_DIR / "installed").exists():
        system.dependency.install_webui_dependency(False)
        system.config.copy_and_load_dotenv()
        (system.config.CONFIG_DIR / "installed").touch()
        seed()

def dump_config():
    """..."""
    print(f"{system.config.CONFIG_DIR = }")
    print(f"{system.config.ROOT = }")

def main(no_run: bool = False):
    """Main Entry"""
    if no_run:
        return

    install()
    system_api = system.webui.api.API()
    window = webview.create_window(
        "RimuTrackRecord - Track all your expenses and income in one go!",
        "data/main.html",
        js_api=system_api,
    )
    system_api.window._define(window)  # pylint: disable=protected-access

    webview.start(debug=True)


if __name__ == "__main__":
    parser = ArghParser()
    parser.add_commands([main, update, clear, install, seed, dump_config, delete_config])
    set_default_command(parser, main)
    parser.dispatch()
