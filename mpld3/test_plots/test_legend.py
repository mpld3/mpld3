"""Plot to test legend"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    fig, ax = plt.subplots()

    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), label='sin', lw=3, alpha=0.5)
    ax.plot(x, np.cos(x), label='cos', lw=3, alpha=0.5)
    ax.plot(x[::5], 0.5 * np.sin(x[::5] + 2), 'ob', label='dots')

    ax.legend(fancybox=True)
    ax.set_title("Legend test", size=20)

    return fig


def test_legend():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
