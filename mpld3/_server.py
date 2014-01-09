"""
A Simple server used to show mpld3 images.
"""
import threading
import webbrowser
import socket
import itertools
import random

try:
    # Python 2.x
    import BaseHTTPServer as server
except ImportError:
    # Python 3.x
    from http import server


def generate_handler(html):
    class MyHandler(server.BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            """Respond to a GET request."""
            self.do_HEAD()
            self.wfile.write("<html><head>"
                             "<title>mpld3 plot</title>"
                             "</head><body>\n")
            self.wfile.write(html)
            self.wfile.write("</body></html>")

    return MyHandler


def find_open_port(ip, port, n=50):
    """Find an open port near the specified port"""
    ports = itertools.chain((port + i for i in range(n)),
                            (port + random.randint(-2 * n, 2 * n)))

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        s.close()
        if result != 0:
            return port
    raise ValueError("no open ports found")


def serve_and_open(html, ip='127.0.0.1', port=8888, n_retries=50):
    """Start a server serving the given HTML, and open a browser

    Parameters
    ----------
    html : string
        HTML to serve
    ip : string (default = '127.0.0.1')
        ip address at which the HTML will be served.
    port : int (default = 8888)
        the port at which to serve the HTML
    n_retries : int (default = 50)
        the number of nearby ports to search if the specified port is in use.
    """
    port = find_open_port(ip, port, n_retries)
    Handler = generate_handler(html)
    srvr = server.HTTPServer((ip, port), Handler)

    # Use a thread to open a web browser pointing to the server
    b = lambda: webbrowser.open('http://{0}:{1}'.format(ip, port))
    threading.Thread(target=b).start()

    # Start the server
    print("Serving to http://{0}:{1}/    [Ctrl-C to exit]".format(ip, port))
    try:
        srvr.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print("\nstopping Server...")

    srvr.server_close()
