import os
from . import __path__
import warnings
#warnings.warn("using temporary MPLD3_URL: switch to ghpages ASAP!")

__all__ = ["D3_URL", "MPLD3_URL", "D3_LOCAL", "MPLD3_LOCAL"]

D3_URL = "http://d3js.org/d3.v3.min.js"

MPLD3_URL = ("https://rawgithub.com/mpld3/mpld3_rewrite/master/"
             "mpld3_rewrite/js/mpld3.v0.1.js")

D3_LOCAL = os.path.join(__path__[0], "js", "d3.v3.min.js")

MPLD3_LOCAL = os.path.join(__path__[0], "js", "mpld3.v0.1.js")
