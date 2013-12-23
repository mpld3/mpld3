__version__ = '0.0.1'
__all__ = ["fig_to_d3", "display_d3", "show_d3"]

from .display import fig_to_d3, display_d3, show_d3


# Add an HTML formatter to IPython if IPython is running so plots
# will automatically display in the notebook. This uses IPython's
# builtin support for the inline backend, so the user still has
# to run %matplotlib inline or %pylab inline. SVG or PNG output
# is still computed so static plots are generated in PDFs.
try:
    from IPython.core.getipython import get_ipython
    from matplotlib.figure import Figure
    ip = get_ipython()
    formatter = ip.display_formatter.formatters['text/html']
    formatter.for_type(Figure, lambda fig: fig_to_d3(fig))
except:
    pass

