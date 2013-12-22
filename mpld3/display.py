import matplotlib.pyplot as plt
from IPython.display import HTML
from . import fig_to_d3


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
    if fig is None:
        fig = plt.gcf()
    if closefig:
        plt.close(fig)
    return HTML(fig_to_d3(fig, d3_url))
