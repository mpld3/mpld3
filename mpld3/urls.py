import os
from . import __path__, __version__
import warnings
#warnings.warn("using temporary MPLD3_URL: switch to ghpages ASAP!")

__all__ = ["D3_URL", "MPLD3_URL", "MPLD3MIN_URL",
           "D3_LOCAL", "MPLD3_LOCAL", "MPLD3MIN_LOCAL"]

WWW_JS_DIR = "http://mpld3.github.io/js/"
D3_URL = "http://d3js.org/d3.v3.min.js"
MPLD3_URL = WWW_JS_DIR + "mpld3.v{0}.js".format(__version__)
MPLD3MIN_URL = WWW_JS_DIR + "mpld3.v{0}.min.js".format(__version__)

LOCAL_JS_DIR = os.path.join(__path__[0], "js")
D3_LOCAL = os.path.join(LOCAL_JS_DIR, "d3.v3.min.js")
MPLD3_LOCAL = os.path.join(LOCAL_JS_DIR,
                           "mpld3.v{0}.js".format(__version__))
MPLD3MIN_LOCAL = os.path.join(LOCAL_JS_DIR,
                              "mpld3.v{0}.min.js".format(__version__))
