"""
Test creation of basic plot elements
"""
import numpy as np
import matplotlib.pyplot as plt
from .. import fig_to_dict, fig_to_html
from numpy.testing import assert_equal


def test_line():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10),
            '--k', alpha=0.3, zorder=10, lw=2)
    rep = fig_to_dict(fig)
    axrep = rep['axes'][0]
    line = axrep['lines'][0]

    assert_equal(list(sorted(line.keys())),
                 ['alpha', 'color', 'coordinates', 'dasharray', 'data',
                  'drawstyle', 'id', 'linewidth', 'xindex', 'yindex',
                  'zorder'])
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
    axrep = rep['axes'][0]
    markers = axrep['markers'][0]

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
    axrep = rep['axes'][0]
    points = axrep['collections'][0]

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


def test_patch():
    fig, ax = plt.subplots()
    ax.add_patch(plt.Rectangle((0, 0), 1, 2, alpha=0.2, linewidth=2,
                               edgecolor='green', facecolor='red', zorder=3))
    rep = fig_to_dict(fig)
    axrep = rep['axes'][0]
    path = axrep['paths'][0]

    assert_equal(list(sorted(path.keys())),
                 ['alpha', 'coordinates', 'dasharray', 'data', 'edgecolor',
                  'edgewidth', 'facecolor', 'id', 'pathcodes',
                  'xindex', 'yindex', 'zorder'])

    assert_equal(path['alpha'], 0.2)
    assert_equal(path['edgecolor'], "#008000")
    assert_equal(path['facecolor'], "#FF0000")
    assert_equal(path['edgewidth'], 2)
    assert_equal(path['zorder'], 3)


def test_text():
    fig, ax = plt.subplots()
    ax.text(0.1, 0.1, "abcde", size=14, color='red', alpha=0.7,
            rotation=15, ha='center', va='center')
    rep = fig_to_dict(fig)
    axrep = rep['axes'][0]
    text = axrep['texts'][0]

    assert_equal(list(sorted(text.keys())),
                 ['alpha', 'color', 'coordinates', 'fontsize', 'h_anchor',
                  'id', 'position', 'rotation', 'text', 'v_baseline',
                  'zorder'])
    assert_equal(text['alpha'], 0.7)
    assert_equal(text['color'], "#FF0000")
    assert_equal(text['text'], "abcde")
    assert_equal(text['rotation'], -15)
    assert_equal(text['fontsize'], 14)
    assert_equal(text['position'], [0.1, 0.1])
    assert_equal(text['h_anchor'], 'middle')
    assert_equal(text['v_baseline'], 'central')
    assert_equal(text['zorder'], 3)
    assert_equal(text['coordinates'], "data")


def test_image():
    fig, ax = plt.subplots()
    ax.imshow(np.random.random((20, 20)), cmap=plt.cm.binary,
              alpha=0.2, zorder=4, extent=(2, 4, 3, 5))
    rep = fig_to_dict(fig)
    axrep = rep['axes'][0]
    image = axrep['images'][0]

    # TODO: how to test data?
    assert_equal(list(sorted(image.keys())),
                 ['alpha', 'coordinates', 'data', 'extent', 'id', 'zorder'])
    assert_equal(image['alpha'], 0.2)
    assert_equal(image['extent'], (2, 4, 3, 5))
    assert_equal(image['zorder'], 4)
    assert_equal(image['coordinates'], "data")


def test_ticks():
    plt.xticks([1,2,3])
    rep = fig_to_html(plt.gcf())
    # TODO: use casperjs here if available to confirm that the xticks
    # are rendeder as expected

    # pandas tslib generates ticks with unusual dtypes
    # test that they are converted to html successfully
    plt.xticks(np.array([1,2,3], dtype=np.int32))
    rep = fig_to_html(plt.gcf())

    # custom ticks should appear in the correct place, with the
    # correct text
    positions, labels = [0, 1, 10], ['A','B','C']
    rep = fig_to_html(plt.gcf())
    # TODO: use casperjs here if available to confirm that the xticks
    # are rendeder as expected
