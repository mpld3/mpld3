from ._objects import D3Figure

def fig_to_d3(fig):
    """Output d3 representation of the figure"""
    return str(D3Figure(fig))
