"""
mpld3 URLs
==========
URLs and filepaths for the mpld3 javascript libraries
"""

import os
from . import __path__, __version__
import warnings

__all__ = ["D3_URL", "MPLD3_URL", "MPLD3MIN_URL",
           "D3_LOCAL", "MPLD3_LOCAL", "MPLD3MIN_LOCAL"]

WWW_JS_DIR = "https://mpld3.github.io/js/"
D3_URL = WWW_JS_DIR + "d3.v3.min.js"
# TODO: Add this to GitHub pages
D3_URL = 'https://d3js.org/d3.v5.js'
MPLD3_URL = WWW_JS_DIR + "mpld3.v{0}.js".format(__version__)
MPLD3MIN_URL = WWW_JS_DIR + "mpld3.v{0}.min.js".format(__version__)

LOCAL_JS_DIR = os.path.join(__path__[0], "js")
D3_LOCAL = os.path.join(LOCAL_JS_DIR, "d3.v5.min.js")
MPLD3_LOCAL = os.path.join(LOCAL_JS_DIR,
                           "mpld3.v{0}.js".format(__version__))
MPLD3MIN_LOCAL = os.path.join(LOCAL_JS_DIR,
                              "mpld3.v{0}.min.js".format(__version__))
