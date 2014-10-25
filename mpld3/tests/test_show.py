"""
Test http server
"""

try:
    # Python 2
    from StringIO import StringIO as IO
except:
    # Python 3
    from io import BytesIO as IO

import matplotlib.pyplot as plt

from .. import show


def test_show():
    """Test mpld3.show() using a mock server"""

    class MockRequest(object):
        def makefile(self, *args, **kwargs):
            return IO(b"GET /")

    class MockServer(object):
        def __init__(self, ip_port, Handler):
            handler = Handler(MockRequest(), ip_port[0], self)

        def serve_forever(self):
            pass

        def server_close(self):
            pass

    # Any exceptions in the show() routine will pop up here
    plt.plot([1, 2, 3])
    show(open_browser=False, http_server=MockServer)
