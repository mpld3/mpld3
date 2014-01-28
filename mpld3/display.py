from ._objects import D3Figure
from ._server import serve_and_open


def fig_to_d3(fig, d3_url=None, **kwargs):
    """Output d3 representation of the figure

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.
    **kwargs :
        Additional keyword arguments passed to D3Figure.html

    Returns
    -------
    fig_html : string
        the HTML representation of the figure

    See Also
    --------
    show_d3 : show a figure in a new browser window, notebook not required.
    display_d3 : embed figure within the IPython notebook
    enable_notebook : automatically embed figures in the IPython notebook
    """
    return D3Figure(fig).html(d3_url=d3_url, **kwargs)


def display_d3(fig=None, closefig=True, d3_url=None):
    """Display figure in IPython notebook via the HTML display hook

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display (grabs current figure if missing)
    closefig : boolean (default: True)
        If true, close the figure so that the IPython matplotlib mode will not
        display the png version of the figure.
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.

    Returns
    -------
    fig_d3 : IPython.display.HTML object
        the IPython HTML rich display of the figure.

    See Also
    --------
    show_d3 : show a figure in a new browser window, notebook not required.
    enable_notebook : automatically embed figures in the IPython notebook
    """
    # import here, in case users don't have requirements installed
    from IPython.display import HTML
    import matplotlib.pyplot as plt
    if fig is None:
        fig = plt.gcf()
    if closefig:
        plt.close(fig)
    return HTML(fig_to_d3(fig, d3_url=d3_url))


def show_d3(fig=None, d3_url=None, ip='127.0.0.1', port=8888, n_retries=50):
    """Open figure in a web browser

    Similar behavior to plt.show().  This opens the D3 visualization of the
    specified figure in the web browser.  On most platforms, the browser
    will open automatically.

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display.  If not specified, the current active figure
        will be used.
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.
    ip : string, default = '127.0.0.1'
        the ip address used for the local server
    port : int, default = 8888
        the port number to use for the local server.  If already in use,
        a nearby open port will be found (see n_retries)
    n_retries : int, default = 50
        the maximum number of ports to try when locating an empty port.

    See Also
    --------
    display_d3 : embed figure within the IPython notebook
    enable_notebook : automatically embed figures in the IPython notebook
    """
    if fig is None:
        # import here, in case matplotlib.use(...) is called by user
        import matplotlib.pyplot as plt
        fig = plt.gcf()

    serve_and_open(D3Figure(fig).html(d3_url=d3_url),
                   ip=ip, port=port, n_retries=n_retries)


def enable_notebook(d3_url=None):
    """Enable the automatic display of figures in the IPython Notebook.

    This function should be used with the inline Matplotlib backend
    that ships with IPython that can be enabled with `%pylab inline`
    or `%matplotlib inline`. This works by adding an HTML formatter
    for Figure objects; the existing SVG/PNG formatters will remain
    enabled.

    Parameters
    ----------
    d3_url : string (optional)
        if specified, then find the d3 library at the provided URL

    See Also
    --------
    disable_notebook : undo this operation
    display_d3 : display a single figure in the notebook
    """
    try:
        from IPython.core.getipython import get_ipython
        from matplotlib.figure import Figure
    except ImportError:
        raise ImportError('This feature requires IPython and Matplotlib')
    ip = get_ipython()
    formatter = ip.display_formatter.formatters['text/html']
    formatter.for_type(Figure, lambda fig: fig_to_d3(fig, d3_url))


def disable_notebook():
    """Disable the automatic display of figures in the IPython Notebook.

    See Also
    --------
    enable_notebook : the operation this function undoes
    """
    try:
        from IPython.core.getipython import get_ipython
        from matplotlib.figure import Figure
    except ImportError:
        raise ImportError('This feature requires IPython and Matplotlib')
    ip = get_ipython()
    formatter = ip.display_formatter.formatters['text/html']
    formatter.type_printers.pop(Figure, None)
