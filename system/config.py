"""Config data"""
from pathlib import Path

CONFIG_DIR = Path("~/.rimueirnarn.rimutrackrecord").expanduser()

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir()

DB_PATH = CONFIG_DIR / "config.db"
ROOT = Path(__file__) / '..' / '..'
