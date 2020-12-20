"""
Test html output
"""
import numpy as np
import matplotlib.pyplot as plt
from .. import fig_to_html, urls
from numpy.testing import assert_equal


def test_html():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10),
            '--ok', alpha=0.3, zorder=10, lw=2)

    d3_url = "http://this.is.a.test/d3.js"
    mpld3_url = "http://this.is.a.test/mpld3.js"

    for template_type in ["simple", "notebook", "general"]:
        html1 = fig_to_html(fig, template_type=template_type)
        html2 = fig_to_html(fig, d3_url, mpld3_url,
                            template_type=template_type)

        # use [:-3] to strip .js from the end (it's not used in require)
        assert urls.D3_URL[:-3] in html1
        assert urls.MPLD3_URL[:-3] in html1
        assert d3_url[:-3] in html2
        assert mpld3_url[:-3] in html2

def test_no_scripts_added():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10),
            '--ok', alpha=0.3, zorder=10, lw=2)
    html = fig_to_html(fig, include_libraries=False)

    assert urls.D3_URL[:-3] not in html
    assert urls.MPLD3_URL[:-3] not in html
