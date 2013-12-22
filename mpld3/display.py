import os
import webbrowser

from ._objects import D3Figure


def fig_to_d3(fig, d3_url=None):
    """Output d3 representation of the figure

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.

    Returns
    -------
    fig_d3 : IPython.display.HTML object
        the IPython HTML rich display of the figure.
    """
    return D3Figure(fig).html(d3_url)


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
    """
    # import here, in case users don't have requirements installed
    from IPython.display import HTML
    import matplotlib.pyplot as plt
    if fig is None:
        fig = plt.gcf()
    if closefig:
        plt.close(fig)
    return HTML(fig_to_d3(fig, d3_url))


def show_d3(fig=None, d3_url=None, tmpfile='_tmp.html'):
    """Open figure in a web browser

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.
    """
    # import here, in case matplotlib.use(...) is called by user
    import matplotlib.pyplot as plt

    if fig is None:
        fig = plt.gcf()

    # TODO: use tempfile; launch simple server so file isn't removed
    f = open(tmpfile, 'w')
    f.write(D3Figure(fig).html(d3_url))

    # TODO: webbrowser.open is unpredictable for local files

    # Open local file (works on OSX; maybe not on others)
    webbrowser.open_new('file://localhost' + os.path.abspath(tmpfile))
