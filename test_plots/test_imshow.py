"""Plot to test imshow"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots()

    x = np.linspace(-2, 2, 20)
    y = x[:, None]
    X = np.zeros((20, 20, 4))

    X[:, :, 0] = np.exp(- (x - 1) ** 2 - (y) ** 2)
    X[:, :, 1] = np.exp(- (x + 0.71) ** 2 - (y - 0.71) ** 2)
    X[:, :, 2] = np.exp(- (x + 0.71) ** 2 - (y + 0.71) ** 2)
    X[:, :, 3] = np.exp(-0.25 * (x ** 2 + y ** 2))

    im = ax.imshow(X, extent=(10, 20, 10, 20),
                   origin='lower')
    fig.colorbar(im, ax=ax)

    ax.set_title('An Image', size=20)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
