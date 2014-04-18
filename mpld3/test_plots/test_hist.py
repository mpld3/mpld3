"""Plot to test polygons"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    fig, ax = plt.subplots()
    ax.grid(color='gray')

    x = np.random.normal(size=500)
    ax.hist(x, 30, fc='blue', alpha=0.5)

    ax.xaxis.set_major_locator(plt.NullLocator())

    return fig


def test_hist():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
