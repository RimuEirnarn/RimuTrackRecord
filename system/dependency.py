"""Webui Dependency Manager"""

import os
import hashlib
import json
from json import JSONDecodeError, loads
from pathlib import Path
from shutil import copy
from zipfile import ZipFile
from tqdm import tqdm
import requests

from .config import ROOT

PATH = Path("data/static/vendor")
TEMP_PATH = ROOT / "temp"


def list_get(array: list, index: int, default):
    """Much like how dict.get() is"""
    try:
        return array[index]
    except IndexError:
        return default


def download_file(url, destination, prefix: str = "", name: str = ""):
    """Download a file with a progress bar using requests and tqdm."""
    response = requests.head(url, timeout=10)
    total_size = int(response.headers.get("content-length", 0))

    with requests.get(url, stream=True, timeout=10) as r, open(destination, "wb") as f:
        r.raise_for_status()
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            desc=prefix + (destination if name == "" else name),
            # ncols=os.terminal_size().columns,
        ) as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                # pbar.ncols
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))


def load_dependencies() -> dict[str, str | list[str, str, bool]]:
    """Load all webui dependencies from its file"""
    deps_path = ROOT / "webui_dependencies.json"
    try:
        data = loads(deps_path.read_text())
        if not isinstance(data, dict):
            raise TypeError("Dependencies has improper setup")
        return data
    except JSONDecodeError:
        return {
            "bootstrap_icons": [
                "https://github.com/twbs/icons/releases/download/v1.11.3/bootstrap-icons-1.11.3.zip",
                "folder",
            ],
            "bootstrap": [
                "https://github.com/twbs/bootstrap/releases/download/v5.3.3/bootstrap-5.3.3-dist.zip",
                "folder",
            ],
            "jquery": ["https://code.jquery.com/jquery-3.6.4.min.js", "file", True],
            "enigmarimu": [
                "https://rimueirnarn.github.io/package-snapshot/enigmarimu.js.zip",
                "folder",
            ],
            "chart.min.js": "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js",
            "chart.umd.js.map": "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js.map",
            "countries.data.json": "https://restcountries.com/v3.1/all?fields=name,currencies",
        }


# def integrity_check():
#     """This only check whether dependencies are stored in vendor. Missing entries are returned"""
#     urls = load_dependencies()

#     for name, rule in urls.items():
#         url = rule if isinstance(rule, str) else rule[0]
#         include_file_extension: bool = (
#             False if isinstance(rule, str) else list_get(rule, 2, False)
#         )
#         action_type = "file" if isinstance(rule, str) else rule[1]

#         file_extension = url.split(".")[-1]
#         _ = str(
#             PATH
#             / f"{name}{'.'+file_extension if (file_extension and include_file_extension and action_type == 'file') or action_type == 'folder' else ''}" # pylint: disable=line-too-long
#         )
#         if (PATH /)


METADATA_PATH = PATH / "installed_dependencies.json"


def calculate_checksum(filepath):
    """Calculate the SHA256 checksum of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except FileNotFoundError:
        return ""


def load_metadata():
    """Load the dependency metadata."""
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_metadata(metadata):
    """Save the dependency metadata."""
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

def clear_cache():
    """Clear download caches"""
    files = os.listdir(TEMP_PATH)
    files.remove("README.md") # for obvious reason, duh
    for (index, file) in enumerate(files):
        os.remove(TEMP_PATH / file)
        print(f'{index+1:0>2} {file} is removed from cache')

def install_webui_dependency(force=False): # pylint: disable=too-many-locals
    """Install Web UI dependencies with update checking."""
    metadata = load_metadata()
    urls = load_dependencies()

    PATH.mkdir(exist_ok=True)
    print("-> Installing/updating webui dependencies")

    for index, (name, rule) in enumerate(urls.items()):
        if isinstance(rule, str):
            url = rule
            action_type = "file"
        else:
            url, action_type, include_file_extension = (
                rule[0],
                rule[1],
                list_get(rule, 2, False),
            )

        response = requests.head(url, timeout=10)
        last_modified = response.headers.get("last-modified")
        fext =  url.split(".")[-1]
        file_extension = (
            "." + fext
            if (fext and include_file_extension and action_type == "file")
            or action_type == "folder"
            else ""
        )  # pylint: disable=line-too-long

        # Use download_file function with progress bar

        destination = str(PATH / (name + file_extension))
        temp = str(TEMP_PATH / (name + file_extension))

        # Skip download if metadata matches
        if not force and name in metadata:
            current_checksum = metadata[name].get("checksum")
            current_modified = metadata[name].get("last_modified")

            if last_modified == current_modified or os.path.exists(temp):
                if current_checksum == calculate_checksum(temp):
                    print(f"  {index:0>2} {name} is up-to-date. Skipping.")
                    continue

        # Download and update metadata
        print(f"  {index+1:0>2} Downloading {name} from {url}...")
        download_file(url, temp, "         ", name)

        if url.endswith(".zip") or action_type == "folder":
            with ZipFile(temp) as zip_file:
                zip_file.extractall(PATH)
                print(f"         {name} extracted to {PATH}")
        if action_type == 'file':
            copy(temp, destination)

        metadata[name] = {
            "url": url,
            "last_modified": last_modified,
            "checksum": calculate_checksum(temp),
        }

    save_metadata(metadata)
    print(f"\n-> Installed/updated: {' '.join(urls.keys())}")
