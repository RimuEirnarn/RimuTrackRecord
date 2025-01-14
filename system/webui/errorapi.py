"""Error API"""

import sys
from types import TracebackType
from traceback import extract_tb

def cast_traceback(tb: TracebackType):
    """Cast Traceback into JSON-friendly object"""
    return [{
        "filename": frame.filename,
        "name": frame.name,
        "line": frame.line,
        "colno": (frame.colno, frame.end_colno),
        "lineno": (frame.lineno, frame.end_lineno),
        "locals": frame.locals
    } for frame in extract_tb(tb)]

def cast_error(error: BaseException):
    """Cast error into JSON-friendly object"""
    return {
        "name": type(error).__name__,
        "value": str(error),
        "notes": error.__notes__,
        "arguments": error.args,
        "cause": cast_error(error.__cause__) if error.__cause__ else None,
        "context": cast_error(error.__context__) if error.__context__ else None,
        "traceback": cast_traceback(error.__traceback__) if error.__traceback__ else []
    }

class ErrorAPI:
    """API to handle and retrieve errors"""
    _errors = []

    @classmethod
    def _log_error(cls, error: BaseException):
        cls._errors.append(cast_error(error))

    @classmethod
    def get_errors(cls):
        """Retrieve all errors"""
        return cls._errors

    @classmethod
    def apply(cls):
        """Apply error handler"""
        def handle_exception(exc_type, exc_value, exc_traceback):
            cls._log_error(exc_value)
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

        sys.excepthook = handle_exception
