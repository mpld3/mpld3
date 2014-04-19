"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np

import mpld3
from mpld3 import plugins


def create_plot():
    fig, ax = plt.subplots()
    line, = ax.plot([0, 1, 3, 8, 5], '-', lw=5)
    plugins.connect(fig, plugins.LineLabelTooltip(line, ['Line A']))
    ax.set_title('Line with Tooltip')
    return fig


def test_line_tooltips():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
