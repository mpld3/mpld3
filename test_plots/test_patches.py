"""Plot to test patches"""
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np


def main():
    fig, ax = plt.subplots()
    ax.grid(color='lightgray')

    rcolor = lambda: np.random.random(3)

    p = [patches.Arrow(0.75, 0.75, 0.5, 0.5),
         patches.Circle((1, 2), 0.4),
         patches.RegularPolygon((1, 3), 5, 0.4),
         patches.Rectangle((1.75, 0.75), 0.7, 0.5)]

    for patch in p:
        patch.set_facecolor(rcolor())
        patch.set_edgecolor(rcolor())
        patch.set_alpha(0.5)
        patch.set_linewidth(2)
        ax.add_patch(patch)

    ax.set_xlim(0.5, 0.5 + 16. / 3.)
    ax.set_ylim(0.5, 4.5)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
