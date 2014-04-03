import mpld3
from mpld3 import plugins
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots(2, 2, sharex='col', sharey='row')

    X = np.random.normal(0, 1, (2, 100))

    for i in range(2):
        for j in range(2):
            points = ax[1 - i, j].scatter(X[i], X[j])

    plugins.connect(fig, plugins.LinkedBrush(points))
    return fig


if __name__ == '__main__':
    fig = main()
    plt.show()
