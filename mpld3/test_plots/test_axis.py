"""Plot to test ticker.FixedFormatter"""

import matplotlib.pyplot as plt
import mpld3


def create_plot():
    positions, labels = [-1, 0, 1, 10, 11], ['OUTSIDE', 'A', 'B', 'C', 'OUTSIDE']
    plt.yticks(positions)
    plt.xticks(positions, labels)
    plt.xlim([0, 10])
    plt.ylim([0, 10])
    return plt.gcf()


def test_axis():
    fig = create_plot()
    _ = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
