"""Plot to test zoom

As a data displayer, I want to control the pan and zoom limits"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots(nrows=2, ncols=2)

    N = 50
    xx = np.random.randn(N)
    yy = np.random.randn(N)

    for i in [0,1]:
        for j in [0,1]:

            points = ax[i,j].plot(xx, yy, 'o', color='k',
                                  mec='w', ms=15, mew=1, alpha=.9)

            ax[i,j].set_xlabel('x')
            ax[i,j].set_ylabel('y')

            zoom = plugins.ConfigurableZoomAndPan(
                ax[i,j], zoom_x=i, zoom_y=j,
                xlim=[-3.5,3.75+i], ylim=[-4, 4.25+j])
            plugins.connect(fig, zoom)

    plugins.connect(fig, plugins.ResetButton())

    return fig

if __name__ == '__main__':
    fig = main()
    print fig_to_d3(fig)

