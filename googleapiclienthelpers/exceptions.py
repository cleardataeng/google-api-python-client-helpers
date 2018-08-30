import httplib2
import socket
import ssl

try:
    from http.client import IncompleteRead, ResponseNotReady
except ImportError:
    from httplib import IncompleteRead, ResponseNotReady

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError


def is_retryable_exception(e):
    # This list comes from forseti
    return isinstance(e, (
        IncompleteRead,
        ResponseNotReady,
        httplib2.ServerNotFoundError,
        socket.error,
        ssl.SSLError,
        URLError,
    ))
