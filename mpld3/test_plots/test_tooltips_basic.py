"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins


def create_plot():
    fig, ax = plt.subplots()
    points = ax.plot(range(10), 'o', ms=20)
    plugins.connect(fig, plugins.PointLabelTooltip(points[0],
                                                   location="top left"))
    return fig


def test_tooltips_basic():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
