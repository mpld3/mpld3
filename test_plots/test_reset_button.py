"""Plot to test reset button plugin"""

user_story = """As a viewer of beautiful mpld3 charts, I would like to
be able to reset a visualization to its initial state. (e.g. origin,
zoom)."""

import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots()
    xx = np.arange(12)
    yy = [3,1,4,1,5,9,2,6,5,3,5,9]

    ax.plot(xx, yy, 'ks-', ms=10, mec='w', mew=3)

    ax.set_title('Reset Button Test', size=14)

    plugins.connect(fig, plugins.ResetButton())
    return fig

if __name__ == '__main__':
    fig = main()
    plt.show()
