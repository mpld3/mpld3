"""
Test Error bars
"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    np.random.seed(1)

    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    xdata = 10 * np.random.random(25)
    dy = 0.2 + 0.2 * np.random.random(xdata.shape)
    ydata = np.random.normal(np.sin(xdata), dy)

    fig, ax = plt.subplots()
    ax.plot(x, y, lw=2, alpha=0.5)
    ax.errorbar(xdata, ydata, dy, fmt='ok', ecolor='gray', label='errors')
    ax.legend()

    return fig


def test_errorbar():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
