"""Window API"""

from webview import Window, OPEN_DIALOG, FOLDER_DIALOG, SAVE_DIALOG
from webview.window import FixPoint

from ..errors import InitiationError

DIALOG_ENUM = {"open": OPEN_DIALOG, "folder": FOLDER_DIALOG, "save": SAVE_DIALOG}

FIXPOINTENUM = {
    "NORTH": FixPoint.NORTH.value,
    "EAST": FixPoint.EAST.value,
    "WEST": FixPoint.WEST.value,
    "SOUTH": FixPoint.SOUTH.value,
}

class WindowAPI:
    """Window API"""

    def _check(self):
        if not self._window:
            raise InitiationError(
                "Window object was not properly defined, _window is null"
            )

    def dialog_enum(self):
        """DIALOG ENUM"""
        return DIALOG_ENUM

    def fixpoint_enum(self):
        """FIX POINT ENUM"""
        return FIXPOINTENUM

    def __init__(self) -> None:
        self._window: Window | None = None

    def height(self):
        """Window height"""
        return self._window.height if self._window else 0

    def weight(self):
        """Window weight"""
        return self._window.width if self._window else 0

    def size(self, size_: tuple[int, int] | None = None):
        """Window size"""
        if not size_:
            return (self._window.width, self._window.height) if self._window else (0, 0)
        self._check()
        self._window.set_window_size(*size_)
        return (-1, -1)

    def title(self, title: str = ""):
        """title"""
        if title == '':
            return self._window.title if self._window else ""
        self.set_title(title)
        return ""

    def on_top(self, set_val: bool | None = None):
        """Get or set on-top property"""
        self._check()
        if set_val is None:
            return self._window.on_top
        self._window.on_top = set_val
        return set_val

    def get_position(self):
        """Get window position"""
        self._check()
        return (self._window.x, self._window.y)

    def _define(self, window: Window):
        self._window = window

    def create_confirmation_dialog(self, title: str, message: str):
        """Create confirmation dialog"""
        self._check()
        return self._window.create_confirmation_dialog(title, message)

    def create_file_dialog(  # pylint: disable=too-many-arguments
        self,
        dialog_type: int = OPEN_DIALOG,
        directory: str = "",
        allow_multiple=False,
        save_filename: str = "",
        filetype=(),
    ):
        """Create file dialogue"""
        self._check()
        ret = self._window.create_file_dialog(
            dialog_type, directory, allow_multiple, save_filename, filetype
        )
        if not ret:
            return tuple()
        if isinstance(ret, str):
            return ret
        return tuple(ret)

    def set_title(self, title: str):
        """Set title"""
        self._check()
        self._window.title = title

    def resize(self, width: int, height: int, fix_point: FixPoint | None = None):
        """Resize"""
        self._check()
        self._window.resize(
            width,
            height,
            FixPoint.NORTH | FixPoint.WEST if not fix_point else fix_point,
        )

    def restore(self):
        """Restore minimized window"""
        self._check()
        self._window.restore()

    def show(self):
        """Show if hidden"""
        self._check()
        self._window.show()

    def toggle_fullscreen(self):
        """Toggle fullscreen"""
        self._check()
        self._window.toggle_fullscreen()

    def maximize(self):
        """Maximize the window"""
        self._check()
        self._window.maximize()

    def minimize(self):
        """Minimize the window"""
        self._check()
        self._window.minimize()

    def move(self, x: int, y: int):
        """Move the window"""
        self._check()
        self._window.move(x, y)

    def native_window(self):
        """Return native window"""
        self._check()
        return self._window.native
