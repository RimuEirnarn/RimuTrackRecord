"""Webui Dependency Manager"""

import os
from json import JSONDecodeError, loads
from pathlib import Path
from typing import Literal
from zipfile import ZipFile
from tqdm import tqdm
import requests

from .config import ROOT

PATH = Path("data/static/vendor")


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
            desc=prefix+(destination if name == "" else name),
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


def install_webui_dependency(force=False):
    """Install Web UI dependencies."""
    if os.path.exists(PATH / "jquery.js") and not force:
        return

    urls = load_dependencies()

    PATH.mkdir(exist_ok=True)
    print("-> Installing webui dependencies")

    for index, seq in enumerate(urls.items()):
        name, rule = seq
        action_type: Literal["file", "folder"] = "file"
        include_file_extension: bool = False
        if isinstance(rule, str):
            url = rule
        if isinstance(rule, (list, tuple)):
            url: str = rule[0]
            action_type: str = rule[1]
            include_file_extension: bool = list_get(rule, 2, False)
        print(f"  {index:0>2} Downloading {name} from {url}...")

        file_extension = url.split(".")[-1]
        destination = str(
            PATH
            / f"{name}{'.'+file_extension if (file_extension and include_file_extension and action_type == 'file') or action_type == 'folder' else ''}"  # pylint: disable=line-too-long
        )

        # Use download_file function with progress bar
        download_file(url, destination, "         ", name)

        if url.endswith(".zip") or action_type == "folder":
            # Unzip the file if it is a zip
            with ZipFile(destination) as zip_file:
                zip_file.extractall(PATH)
                print(f"         {name} extracted to {PATH}")
            os.remove(destination)  # Clean up the zip file after extraction
        else:
            print(f"         {name} saved to {destination}")

    print(f"\n-> Installed: {' '.join(urls.keys())}")
