"""Profile handler"""

from json import loads
from pathlib import Path
from traceback import format_exception
from urllib.parse import urlparse
from typing import NamedTuple, Callable, Any

import system.log
from ...database import system_config
from .validation import Validation, to_text

OptStr = str | None
OptInt = int | None
default = object()
_DELOBJS_CW = ["js_api", "server", "server_args", "localization"]
_DELOBJS_S = ["func", "server", "server_args", "menu"]
_STR_DEFKEY = "py:default"
_DELOBJS_API = ["html", "http_server", "http_port", "storage_path", "ssl", "args"]


def get_config() -> dict[str, Any]:
    """Get system config"""
    data = system_config.select()
    return {a.name: loads(a.value) for a in data}


def check(name):
    """Check if name contains illegal characters"""
    if "/" in name:
        return False
    if "\\" in name:
        return False
    return True


class CWConfig(NamedTuple):
    """Create Window Config"""

    title: str = ""
    url: OptStr = None
    html: OptStr = None
    js_api: OptStr = None
    width: int = 800
    height: int = 600
    x: OptInt = None
    y: OptInt = None
    resizable: bool = True
    fullscreen: bool = False
    hidden: bool = False
    frameless: bool = False
    easy_drag: bool = True
    minimized: bool = False
    on_top: bool = False
    confirm_close: bool = False
    background_color: str = "#FFFFFF"
    transparent: bool = False
    text_select: bool = False
    zoomable: bool = False
    draggable: bool = False
    server: Any = default
    server_args: dict | Any = default
    localization: dict | None = None

    def validate(self):
        """Validate create-window configs"""
        vl = Validation()
        vl.set(isinstance(self.title, str), "app/title", "Title is not a string")
        r = urlparse(self.url)
        vl.set(
            (all((r.scheme, r.netloc)) and self.html is None) or Path(self.url or "").exists(),
            "app/url",
            "URL is malformed",
        )
        # HTML is optional
        vl.set(isinstance(self.width, int), "app/width", "the width is not an integer")
        vl.set(
            isinstance(self.height, int),
            "app/height",
            "the height is not an integer",
        )
        vl.set(self.width > 0, "app/width", "width must not less than 0")
        vl.set(self.height > 0, "app/height", "height must not less than 0")
        # X, Y is optional
        vl.set(
            all(
                map(
                    lambda stuff: isinstance(stuff, bool),
                    (
                        self.resizable,
                        self.fullscreen,
                        self.hidden,
                        self.frameless,
                        self.easy_drag,
                        self.minimized,
                        self.on_top,
                        self.confirm_close,
                        self.transparent,
                        self.text_select,
                        self.zoomable,
                        self.draggable,
                    ),
                )
            ),
            "app/bools",
            "A value is detected to be non-boolean",
        )
        vl.set(
            self.background_color[0] == "#" and len(self.background_color) == 7,
            "app/background_color",
            "Color format is invalid",
        )
        return vl


class StartConfig(NamedTuple):
    """Start config"""

    func: Callable[[...], Any] | None = None  # type: ignore
    args: Any | tuple[Any, ...] | None = None
    localization: dict | None = None
    gui: OptStr = None
    debug: bool = False
    http_server: bool = False
    http_port: bool = False
    user_agent: str | None = None
    private_mode: bool = True
    storage_path: str | None = None
    menu: list | Any = default
    server: Any = default
    ssl: bool = False
    server_args: dict | Any = default

    def validate(self):
        """Validate start config"""
        vl = Validation()
        vl.set(
            all(
                map(
                    lambda stuff: isinstance(stuff, bool),
                    (self.debug, self.private_mode),
                )
            ),
            "start/any",
            "Either debug/private mode is not boolean",
        )
        return vl


class WebviewSetting(NamedTuple):
    """Webview Setting"""

    ALLOW_DOWNLOADS: bool = False
    ALLOW_FILE_URLS: bool = True
    ALLOW_EXTERNAL_LINKS_IN_BROWSER: bool = True
    OPEN_DEVTOOL_IN_DEBUG: bool = True

    def validate(self):
        """Webview config validator"""
        assert all(map(lambda stuff: isinstance(stuff, bool), self))


def replace_default(ns: dict[str, Any], with_: Any):
    """Replace constant default with others"""
    copied = ns.copy()
    for k in ns.copy():
        if copied[k] is default:
            copied[k] = with_
    return copied


def annihilate_defconst(ns: dict[str, Any], to_api: bool = False):
    """Delete any constant default"""
    copied = ns.copy()
    for k in ns.copy():
        if ns[k] is default or ns[k] == _STR_DEFKEY:
            del copied[k]
            continue
        if k in _DELOBJS_CW or k in _DELOBJS_S:
            del copied[k]
        if to_api and k in _DELOBJS_API:
            del copied[k]
    return copied


def create_configs_from_dict(
    config_dict: dict,
) -> tuple[CWConfig, StartConfig, WebviewSetting]:
    """
    Process a flat config dictionary into CWConfig, StartConfig, and WebviewSetting objects.

    Args:
        config_dict: Flat dictionary from get_config()

    Returns:
        Tuple of (CWConfig, StartConfig, WebviewSetting) objects
    """
    # Define prefixes/namespaces for each config type
    cw_fields = set(CWConfig._fields)
    start_fields = set(StartConfig._fields)
    setting_fields = set(WebviewSetting._fields)

    # Initialize dictionaries for each config type
    cw_dict = {}
    start_dict = {}
    setting_dict = {}

    # Sort config items into appropriate dictionaries
    for key, value in config_dict.items():
        if key in cw_fields:
            cw_dict[key] = value
        elif key in start_fields:
            start_dict[key] = value
        elif key in setting_fields:
            setting_dict[key] = value

    _cw_default = annihilate_defconst(CWConfig()._asdict())
    _st_config = annihilate_defconst(StartConfig()._asdict())
    _webview_setting = annihilate_defconst(WebviewSetting()._asdict())

    # Create objects with defaults for missing fields
    cw_config = CWConfig(**{**_cw_default, **cw_dict})
    start_config = StartConfig(**{**_st_config, **start_dict})
    webview_setting = WebviewSetting(**{**_webview_setting, **setting_dict})

    return cw_config, start_config, webview_setting


class Profile:
    """Profile for webapps. Options will follow pywebview.create_window"""

    def __init__(self, url: str, title: str = None):
        self._data = CWConfig(title, url=url)
        self._start_data = StartConfig(private_mode=False, storage_path=None)
        self._webview_config = WebviewSetting()

    @property
    def data(self):
        """Return data used for webapps"""
        return self._data

    @property
    def start_data(self):
        """Return data used for starting webapps"""
        return self._start_data

    @property
    def webview_data(self):
        """Return webview setting"""
        return self._webview_config

    def to_dict(self):
        """Return the instance into JSON-able"""
        return {
            "app": annihilate_defconst(self.data._asdict(), True),
            "start": annihilate_defconst(self.start_data._asdict(), True),
            "config": annihilate_defconst(self._webview_config._asdict(), True),
        }

    def update_from_config(self):
        """Update configs from system config"""
        try:
            config_dict = get_config()
            self._data, self._start_data, self._webview_config = (
                create_configs_from_dict(config_dict)
            )

            # Validate the new configs
            validation_results = self.validate()
            if validation_results:
                # Handle validation errors
                system.log.error("Invalid configuration: %s", to_text(validation_results))
                raise ValueError(f"Invalid configuration: {to_text(validation_results)}")

        except Exception as e:
            # Handle any errors during config processing
            system.log.error("Failed to update configuration: %s", str(e))
            system.log.error("".join(format_exception(e)))
            raise RuntimeError(f"Failed to update configuration: {str(e)}") from e

    def validate(self):
        """Validate this profile"""
        vl = Validation()
        # vl.set(False, "name", "test :3")
        vl1 = self.data.validate()
        vl2 = self.start_data.validate()
        self._webview_config.validate()
        a0 = vl.to_json()
        a0.extend(vl1.to_json())
        a0.extend(vl2.to_json())
        return a0
