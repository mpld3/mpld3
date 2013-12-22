"""Plot to test logscale"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots(2, 2)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    x = np.linspace(1e-3, 1e3)
    y = x ** 2

    ax[0, 0].plot(x, y)
    ax[0, 1].semilogx(x, y)
    ax[1, 0].semilogy(x, y)
    ax[1, 1].loglog(x, y)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
