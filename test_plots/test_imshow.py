"""Plot to test imshow"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots()

    x = np.linspace(-2, 2, 20)
    y = x[:, None]
    X = np.zeros((20, 20, 4))

    X[:, :, 0] = np.exp(- (x - 1) ** 2 - (y) ** 2)
    X[:, :, 1] = np.exp(- (x + 0.71) ** 2 - (y - 0.71) ** 2)
    X[:, :, 2] = np.exp(- (x + 0.71) ** 2 - (y + 0.71) ** 2)
    X[:, :, 3] = np.exp(-0.25 * (x ** 2 + y ** 2))

    im = ax.imshow(X, extent=(10, 20, 10, 20),
                   origin='lower', zorder=1, interpolation='nearest')
    fig.colorbar(im, ax=ax)

    ax.text(16, 16, "overlaid text")
    ax.text(16, 15, "covered text", zorder=0)

    ax.set_title('An Image', size=20)
    ax.set_xlim(9, 21)
    ax.set_ylim(9, 21)

    plugins.connect(fig, plugins.ConfigurableZoomAndPan(ax, xlim=(9,21), ylim=(9,21)))
    plugins.connect(fig, plugins.ResetButton())

    return fig

if __name__ == '__main__':
    fig = main()
    print fig_to_d3(fig)
