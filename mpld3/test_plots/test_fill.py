"""Plot to test text"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    fig, ax = plt.subplots()
    ax.grid(color='lightgray')

    x = np.linspace(0, 4 * np.pi, 1000)
    y1 = 0.5 * np.sin(0.5 * x)
    y2 = np.sin(x)
    y3 = np.cos(x)

    y1[450:550] = np.nan

    ax.fill(x, y1, alpha=0.3, facecolor='green')
    ax.fill_between(x, y2, y3, alpha=0.3, facecolor='red')
    ax.fill_between(x, -y2, -y3, alpha=0.3, facecolor='blue')

    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(-1.1, 1.1)

    ax.set_title("fill() and fill_between()", size=18)
    return fig


def test_fill():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
