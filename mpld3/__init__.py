"""
Interactive D3 rendering of matplotlib images
=============================================

Functions: General Use
----------------------
- :func:`fig_to_html` : convert a figure to an html string

- :func:`fig_to_dict` : convert a figure to a dictionary representation

- :func:`save_html` : save a figure to an html file

- :func:`save_json` : save a JSON representation of a figure to file

- :func:`show` : launch a web server to view an d3/html figure representation


Functions: IPython Notebook
---------------------------
- :func:`display` : display a figure in an IPython notebook

- :func:`enable_notebook` : enable automatic D3 display of figures
                            in the IPython notebook.

- :func:`disable_notebook` : disable automatic D3 display of figures
                             in the IPython
"""

__version__ = '0.1'

from .urls import *
from ._display import *
