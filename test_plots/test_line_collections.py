"""Plot to test line collections"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

def main():
    t = np.linspace(0, 10, 100)
    x = np.cos(np.pi * t)
    y = np.sin(t)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(segments, cmap=plt.get_cmap('copper'),
        norm=plt.Normalize(0, 10))
    lc.set_array(t)
    lc.set_linewidth(3)

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    ax.set_title("Line Collections", size=18)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
