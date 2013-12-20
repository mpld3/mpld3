"""Plot to test polygons"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots()
    ax.grid(color='gray')

    x = np.random.normal(size=500)
    ax.hist(x, 30, fc='blue', alpha=0.5)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
