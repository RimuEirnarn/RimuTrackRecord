'''main'''
from argh import dispatch_command
import webview
import system.database
import system.webui.api
import system.config
import system.configstore
import system.dependency


def main(redownload: bool = False, no_run: bool = False):
    """Main Entry"""
    system.dependency.install_webui_dependency(redownload)
    if no_run:
        return
    system_api = system.webui.api.API()
    window = webview.create_window(
        "RimuTrackRecord - Track all your expenses and income in one go!",
        "data/main.html",
        js_api=system_api,
    )
    system_api.window._define(window) # pylint: disable=protected-access

    webview.start(debug=True)

if __name__ == '__main__':
    dispatch_command(main)
