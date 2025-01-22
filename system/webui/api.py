"""Webview API"""

import sys

from ..config import PROD
from ..database import transaction
from .configapi import ConfigAPI
from .database import DatabaseAPI
from .systemapi import SystemAPI
from .stringapi import String
from .errorapi import ErrorAPI
from .window import WindowAPI
from ..configstore import system_config

class API:
    """Entry Level API"""
    database = DatabaseAPI()
    sys = SystemAPI()
    config = ConfigAPI()
    sys_config = ConfigAPI(system_config)
    str = String()
    error = ErrorAPI()
    window = WindowAPI()

    init_error = False

    def is_prod(self):
        """Return if the application is in production"""
        return PROD

    def __init__(self):
        self._setup_global_error_handler()

    def _setup_global_error_handler(self):
        # print("Reached here")
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            self.error._log_error(exc_value) # pylint: disable=protected-access

        sys.excepthook = handle_exception

    def retrieve_current_savings(self):
        """Return current money/savings from all transactions"""
        s: float = transaction.select(only='amount')
        return sum(s)

    def exit(self):
        """Exit"""
        sys.exit(0)
