"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots()

    np.random.seed(0)
    numPoints=10

    xx = np.arange(numPoints, dtype=float)
    xx[6] = np.nan

    yy = np.random.normal(size=numPoints)
    yy[3] = np.nan

    ax.plot(xx, yy, 'ks-', ms=10, mec='w', mew=3)

    ax.set_xlabel('x has uniform spacing')
    ax.set_ylabel('y includes a nan')
    ax.set_title('NaN test', size=14)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
