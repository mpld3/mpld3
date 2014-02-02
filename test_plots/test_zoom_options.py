"""Plot to test zoom

As a data displayer, I want to control the pan and zoom limits"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots()

    N = 50
    xx = np.random.randn(N)
    yy = np.random.randn(N)

    points = ax.plot(xx, yy, 'o', color='k', mec='w', ms=15, mew=1, alpha=.9)

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plugins.connect(fig, plugins.Zoom())
    plugins.connect(fig, plugins.ResetButton())

    return fig

if __name__ == '__main__':
    fig = main()
    print fig_to_d3(fig)

