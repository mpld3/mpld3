"""Plot to test ticker.FixedFormatter"""

import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    positions, labels = [0, 1, 10], ['A','B','C']
    plt.xticks(positions, labels)
    return plt.gcf()


def test_axis():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
