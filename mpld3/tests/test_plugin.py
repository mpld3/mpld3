"""
Test plugins
"""
import numpy as np
import matplotlib.pyplot as plt
from .. import fig_to_html, plugins
from numpy.testing import assert_equal


class FakePlugin(plugins.PluginBase):
    JAVASCRIPT = """TEST--this is the javascript--TEST"""

    def __init__(self, fig):
        self.fig = fig
        self.dict_ = {}
        self.css_ = """TEST--this is the css--TEST"""


def test_plugins():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10),
            '--ok', alpha=0.3, zorder=10, lw=2)
    plug = FakePlugin(fig)
    plugins.connect(fig, plug)

    for template_type in ["simple", "notebook", "general"]:
        html = fig_to_html(fig, template_type=template_type)
        assert plug.JAVASCRIPT in html
        assert plug.css_ in html
