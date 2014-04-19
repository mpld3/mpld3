"""Plot to test line contours"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import mpld3


def create_plot():
    x = np.linspace(-3.0, 3.0, 30)
    y = np.linspace(-2.0, 2.0, 30)
    X, Y = np.meshgrid(x, y)
    Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
    Z = 10.0 * (Z2 - Z1)

    fig, ax = plt.subplots()
    CS = ax.contourf(X, Y, Z, 30)
    return fig


def test_contourf():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
