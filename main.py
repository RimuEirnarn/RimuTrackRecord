'''main'''
from argh import ArghParser, set_default_command
import webview
import system.database
import system.webui.api
import system.config
import system.configstore
import system.dependency

def clear():
    """Clear all webui dependency caches"""
    system.dependency.clear_cache()

def update():
    """Update webui dependency if necessary"""
    system.dependency.install_webui_dependency()

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
    parser = ArghParser()
    parser.add_commands([main, update, clear])
    set_default_command(parser, main)
    parser.dispatch()
