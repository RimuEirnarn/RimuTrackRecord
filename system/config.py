"""Config data"""

from os import environ
from shutil import copyfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PROD = environ.get("production", "false") == "true"
ROOT = (Path(__file__) / ".." / "..").resolve()
CONFIG_DIR = (
    Path("~/.rimueirnarn.rimutrackrecord").expanduser()
    if PROD
    else (ROOT / "temp" / "profile").resolve()
)

def copy_and_load_dotenv():
    """Load dotenv"""
    copyfile(ROOT / "example.env", ROOT / ".env")
    load_dotenv()

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir()

DB_PATH = CONFIG_DIR / "config.db"
