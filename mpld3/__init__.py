__all__ = ["fig_to_d3", "display_d3"]

from ._objects import D3Figure
from .display import display_d3

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

