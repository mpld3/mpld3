"""
Test creation of basic plot elements
"""
import numpy as np
import matplotlib.pyplot as plt
from .. import fig_to_dict
from numpy.testing import assert_equal


def test_line():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10),
            '--k', alpha=0.3, zorder=10, lw=2)
    rep = fig_to_dict(fig)
    ax = rep['axes'][0]
    line = ax['lines'][0]

    assert_equal(list(sorted(line.keys())),
                 ['alpha', 'color', 'coordinates', 'dasharray', 'data', 'id',
                  'linewidth', 'xindex', 'yindex', 'zorder'])
    assert_equal(line['alpha'], 0.3)
    assert_equal(line['color'], "#000000")
    assert_equal(line['coordinates'], 'data')
    assert_equal(line['dasharray'], '6,6')
    assert_equal(line['zorder'], 10)
    assert_equal(line['linewidth'], 2)


def test_markers():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10),
            '^k', alpha=0.3, zorder=10, mec='r', mew=2, c='b')
    rep = fig_to_dict(fig)
    ax = rep['axes'][0]
    markers = ax['markers'][0]

    assert_equal(list(sorted(markers.keys())),
                 ['alpha', 'coordinates', 'data', 'edgecolor', 'edgewidth',
                  'facecolor', 'id', 'markerpath', 'xindex', 'yindex',
                  'zorder'])
    assert_equal(markers['alpha'], 0.3)
    assert_equal(markers['zorder'], 10)
    assert_equal(markers['coordinates'], 'data')
    assert_equal(markers['edgecolor'], '#FF0000')
    assert_equal(markers['edgewidth'], 2)
    assert_equal(markers['facecolor'], '#0000FF')
    assert_equal(markers['markerpath'][0],
                 [[0.0, -3.0], [-3.0, 3.0], [3.0, 3.0]])
    assert_equal(markers['markerpath'][1],
                 ['M', 'L', 'L', 'Z'])


def test_scatter():
    fig, ax = plt.subplots()
    ax.scatter(np.arange(10), np.random.random(10), c='r', s=30,
               marker='^', alpha=0.3, lw=2, edgecolors='b', zorder=10)
    rep = fig_to_dict(fig)
    ax = rep['axes'][0]
    points = ax['collections'][0]

    assert_equal(list(sorted(points.keys())),
                 ['alphas', 'edgecolors', 'edgewidths', 'facecolors', 'id',
                  'offsetcoordinates', 'offsets', 'pathcoordinates', 'paths',
                  'pathtransforms', 'xindex', 'yindex', 'zorder'])
    assert_equal(points['alphas'], [0.3])
    assert_equal(points['zorder'], 10)
    assert_equal(points['edgecolors'], ['#0000FF'])
    assert_equal(points['facecolors'], ['#FF0000'])
    assert_equal(points['edgewidths'], (2.0,))
    assert_equal(points['paths'][0][0],
                 [[0.0, 0.5], [-0.5, -0.5], [0.5, -0.5]])
    assert_equal(points['paths'][0][1],
                 ['M', 'L', 'L', 'Z'])
    assert_equal(points['pathtransforms'],
                 [[6.085806194501846, 0.0, 0.0, 6.085806194501846, 0.0, 0.0]])
