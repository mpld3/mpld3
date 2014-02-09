"""Plot to test mouse position plugin

As a data explorer, I would like to know the precise coordinates of my
cursor on a graph."""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    N = 5

    fig, ax = plt.subplots(2, 2, sharex=False, sharey=False)
    fig.subplots_adjust(hspace=0.3)

    for i in range(2):
        for j in range(2):
            txt = '({i}, {j})'.format(i=i, j=j)
            ax[i, j].set_title(txt, size=14)
            ax[i, j].plot(10**i * 100**j * np.random.randn(N),
                          10**i * 100**j * np.random.randn(N),
                          'o-', mec='w', mew=3)
            ax[i, j].grid(True, color='lightgray')
            ax[i, j].set_xlabel('xlabel')
            ax[i, j].set_ylabel('ylabel')

    plugins.connect(fig, plugins.MousePosition(), plugins.ResetButton())
    return fig

if __name__ == '__main__':
    fig = main()
    print fig_to_d3(fig)
