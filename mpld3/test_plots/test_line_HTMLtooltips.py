"""Plot to test HTML line tooltip"""
import matplotlib.pyplot as plt

import mpld3
from mpld3 import plugins


def create_plot():
    fig, ax = plt.subplots()
    line, = ax.plot([0, 1, 3, 8, 5], '-', lw=5)
    label = '<h1>Line {}</h1>'.format('A')
    plugins.connect(fig, plugins.LineHTMLTooltip(line, label))
    ax.set_title('Line with HTML Tooltip')
    return fig


def test_line_tooltips():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
