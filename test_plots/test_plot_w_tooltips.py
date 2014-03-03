"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins

def main():
    fig, ax = plt.subplots()
    points = ax.plot(range(10), 'o', ms=20)
    plugins.connect(fig, plugins.PointLabelTooltip(points[0],
                                                   location="top left"))

    return fig

if __name__ == '__main__':
    fig = main()
    plt.show()

