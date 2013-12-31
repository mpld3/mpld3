"""Plot to test patches"""
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.path import Path
import numpy as np


def main():
    fig, ax = plt.subplots()
    ax.grid(color='lightgray')

    rcolor = lambda: np.random.random(3)

    # The points are scaled to be between 0 and 1 in both x and y
    # Shift to be between 3.5 and 4.5 in x and .5 to 1.5 in y
    points = np.loadtxt('test_plots/coords_test_patch.txt')
    points += [3.5,.5]
    codes = [Path.LINETO] * len(points)
    codes[0] = Path.MOVETO

    p = [patches.Arrow(0.75, 0.75, 0.5, 0.5),
         patches.Circle((1, 2), 0.4),
         patches.RegularPolygon((1, 3), 5, 0.4),
         patches.Rectangle((1.6, 0.75), 0.8, 0.5),
         patches.CirclePolygon((2, 2), 0.4),
         patches.Polygon([[1.75, 3], [2, 3.25], [2.25, 3],
                          [2, 2.75], [1.75, 3]]),
         patches.Wedge((3, 1), 0.4, 0, 270),
         patches.Ellipse((3, 2), 0.6, 0.4),
         patches.Arc((3, 3), 0.5, 0.5, 270, 90),
         patches.PathPatch(Path(points, codes))
    ]

    for patch in p:
        patch.set_facecolor(rcolor())
        patch.set_edgecolor(rcolor())
        patch.set_alpha(0.5)
        patch.set_linewidth(2)
        ax.add_patch(patch)

    # add a static patch
    ax.add_patch(patches.Rectangle((0.3, 0.3), 0.4, 0.4,
                                   fc='yellow', ec='black', alpha=0.3,
                                   transform=ax.transAxes))

    # make sure axes ratio is equal
    ax.set_xlim(0.5, 0.5 + 3. * 4. / 3.)
    ax.set_ylim(0.5, 3.5)

    ax.set_title("Various Patches", size=16)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
