"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins


def create_plot():
    fig, ax = plt.subplots()
    colors = plt.rcParams['axes.color_cycle']
    points = []

    for i, color in enumerate(colors):
        points = ax.plot(i, 0, 'o', c=color, ms=20)
        plugins.connect(fig,
                        plugins.PointLabelTooltip(points[0], [color]))
    ax.set_xlim(-1, len(colors) + 1)
    return fig


def test_tooltips_labels():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
