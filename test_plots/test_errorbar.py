"""
Test Error bars
"""
import matplotlib.pyplot as plt
import numpy as np

from mpld3 import show_d3


def main():
    np.random.seed(1)

    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    xdata = 10 * np.random.random(25)
    dy = 0.2 + 0.2 * np.random.random(xdata.shape)
    ydata = np.random.normal(np.sin(xdata), dy)
    
    fig, ax = plt.subplots()
    ax.plot(x, y, lw=2, alpha=0.5)
    ax.errorbar(xdata, ydata, dy, fmt='ok', ecolor='gray')
    
    return fig


if __name__ == '__main__':
    fig = main()
    show_d3()
