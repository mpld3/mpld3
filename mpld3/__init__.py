__all__ = ["fig_to_d3"]

from ._objects import D3Figure

def fig_to_d3(fig, d3_location=None):
    """Output d3 representation of the figure"""
    return D3Figure(fig).html(d3_location)
