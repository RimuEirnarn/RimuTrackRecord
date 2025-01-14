"""SystemAPI"""

from os import listdir
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent.parent / "data"

class SystemAPI:
    """System API"""

    def list_files(self, path: str) -> list:
        """List files in a directory"""

        if path == '':
            return listdir(BASE_PATH)

        npath = BASE_PATH / path
        # print(npath)
        if not str(npath).startswith(str(BASE_PATH)):
            raise ValueError("Is not allowed to travel outside the base directory")

        return listdir(npath)

    def list_base_files(self) -> list:
        """List files in the base directory"""

        return listdir(BASE_PATH)

    def read_file(self, path: str) -> str:
        """Read a file"""

        npath = BASE_PATH / path
        if not str(npath).startswith(str(BASE_PATH)):
            raise ValueError("Is not allowed to travel outside the base directory")

        with open(npath, encoding='utf-8') as f:
            return f.read()

    def redownload_webui_dependency(self):
        """Redownload Web UI dependencies"""

        # pylint: disable-next=import-outside-toplevel
        from system.dependency import install_webui_dependency

        print("Downloading?")
        install_webui_dependency(force=True)

    def raise_me(self):
        """Raise an error"""

        raise ValueError("This is an self-test error")
