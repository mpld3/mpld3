import os
from ..urls import MPLD3_LOCAL, MPLD3MIN_LOCAL, D3_LOCAL


def test_js_libs_exist():
    for jsfile in [MPLD3_LOCAL, MPLD3MIN_LOCAL, D3_LOCAL]:
        assert os.path.exists(jsfile)
