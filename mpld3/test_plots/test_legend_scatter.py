"""Plot to test legend"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    fig, ax = plt.subplots()

    x = np.linspace(0, 10, 100)
    ax.scatter(x, np.sin(x), label='sin', alpha=0.5)
    ax.scatter(x, np.cos(x), label='cos',  c='g', alpha=0.5)
    ax.scatter(x[::5], 0.5 * np.sin(x[::5] + 2), c='b', label='dots')

    ax.legend(fancybox=True)
    ax.set_title("Legend Scatter test", size=20)

    return fig


def test_legend():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
