"""Plot to test logscale"""
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, wspace=0.4)

    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, sharey=ax1, xscale='log')
    ax3 = fig.add_subplot(2, 2, 3, sharex=ax1, yscale='log')
    ax4 = fig.add_subplot(2, 2, 4, sharex=ax2, sharey=ax3)

    x = np.linspace(1, 1e2)
    y = x ** 2

    for ax in [ax1, ax2, ax3, ax4]:
        ax.plot(x, y)

    plugins.connect(fig, plugins.ResetButton(), plugins.Debug())
    return fig

if __name__ == '__main__':
    fig = main()
    print fig_to_d3(fig)
