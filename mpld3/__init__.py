"""
Interactive D3 rendering of matplotlib images
=============================================

Functions: General Use
----------------------
:func:`fig_to_html`
    convert a figure to an html string

:func:`fig_to_dict`
    convert a figure to a dictionary representation

:func:`show`
    launch a web server to view an d3/html figure representation

:func:`save_html`
    save a figure to an html file

:func:`save_json`
    save a JSON representation of a figure to file


Functions: IPython Notebook
---------------------------
:func:`display`
    display a figure in an IPython notebook

:func:`enable_notebook`
    enable automatic D3 display of figures in the IPython notebook.

:func:`disable_notebook`
    disable automatic D3 display of figures in the IPython
"""

import os
import matplotlib

if os.environ.get('HIDE_PLOTS', False):
    matplotlib.use('Agg') 

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BIN_PATH = os.path.join(BASE_PATH, "bin/") 

SCREENSHOT_BIN = os.path.join(BIN_PATH, "screenshot")

__all__ = ["__version__",
           "fig_to_html", "fig_to_dict", "fig_to_d3", "display_d3",
           "display", "show_d3", "show", "save_html", "save_json",
           "enable_notebook", "disable_notebook", "plugins", "urls"]

from .__about__ import __version__
from . import plugins
from . import urls
from ._display import *
