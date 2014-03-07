import os
from . import __path__
import warnings
#warnings.warn("using temporary MPLD3_URL: switch to ghpages ASAP!")

__all__ = ["D3_URL", "MPLD3_URL", "D3_LOCAL", "MPLD3_LOCAL"]

D3_URL = "http://d3js.org/d3.v3.min.js"

MPLD3_URL = "http://mpld3.github.io/js/mpld3.v0.2git.js"

D3_LOCAL = os.path.join(__path__[0], "js", "d3.v3.min.js")

MPLD3_LOCAL = os.path.join(__path__[0], "js", "mpld3.v0.2git.js")
