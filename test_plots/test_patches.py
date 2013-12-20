"""Plot to test patches"""
import matplotlib.pyplot as plt
from matplotlib import patches

def main():
    fig, ax = plt.subplots()
    ax.grid(color='lightgray')

    ax.add_patch(patches.Arrow(0.75, 0.75, 0.5, 0.5,
                               facecolor='blue',
                               edgecolor='black', alpha=0.5))

    ax.add_patch(patches.Circle((1, 2), 0.5,
                                facecolor='green',
                                edgecolor='gray',
                                alpha=0.5))

    ax.add_patch(patches.RegularPolygon((1, 3), 5, 0.5,
                                        facecolor='cyan',
                                        edgecolor='blue'))

    ax.set_xlim(0.5, 0.5 + 16. / 3.)
    ax.set_ylim(0.5, 4.5)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
