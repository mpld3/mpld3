"""Plot to test line collections"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
import mpld3


def create_plot():
    t = np.linspace(0, 10, 100)
    x = 0.1 * t * np.cos(np.pi * t)
    y = 0.1 * t * np.sin(np.pi * t)
    points = np.array([x, y]).T.reshape(100, 1, 2)
    segments = np.hstack([points[:-1], points[1:]])

    lc = LineCollection(segments, cmap=plt.cm.jet,
                        norm=plt.Normalize(0, 10),
                        array=t, linewidths=3)

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    ax.set_title("Line Collections", size=18)

    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.yaxis.set_major_formatter(plt.NullFormatter())
    return fig


def test_line_collections():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
