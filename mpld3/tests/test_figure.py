"""
Test creation of a figure
"""
import matplotlib.pyplot as plt
from .. import fig_to_dict
from numpy.testing import assert_equal


def test_basic_figure():
    size = (8, 6)
    dpi = 80
    fig = plt.figure(figsize=size, dpi=dpi)
    rep = fig_to_dict(fig)
    plt.close(fig)

    assert_equal(list(sorted(rep.keys())),
                 ['axes', 'data', 'height', 'id', 'plugins', 'width'])
    assert_equal(rep['width'], size[0] * dpi)
    assert_equal(rep['height'], size[1] * dpi)
    assert_equal(rep['data'], {})
    assert_equal(rep['axes'], [])


def test_axes():
    bbox = [0.1, 0.1, 0.8, 0.8]
    xlim = [-10, 10]
    ylim = [-20, 20]

    fig = plt.figure()
    ax = fig.add_axes(bbox)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    rep = fig_to_dict(fig)
    axrep = rep['axes'][0]

    assert_equal(list(sorted(axrep.keys())),
                 ['axes', 'axesbg', 'axesbgalpha', 'bbox', 'collections',
                  'id', 'images', 'lines', 'markers', 'paths', 'sharex',
                  'sharey', 'texts', 'xdomain', 'xlim', 'xscale', 'ydomain',
                  'ylim', 'yscale', 'zoomable'])

    for key in ['collections', 'images', 'lines', 'markers', 'paths', 'texts']:
        assert_equal(axrep[key], [])

    for key in ['xlim', 'xdomain']:
        assert_equal(axrep[key], xlim)

    for key in ['ylim', 'ydomain']:
        assert_equal(axrep[key], ylim)

    for key in ['xscale', 'yscale']:
        assert_equal(axrep[key], 'linear')

    assert_equal(axrep['zoomable'], True)

    assert_equal(axrep['bbox'], bbox)
