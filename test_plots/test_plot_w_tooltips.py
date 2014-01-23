"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots()
    points = ax.plot(range(10), 'o')
    plugins.connect(fig, plugins.PointLabelTooltip(points[0]))

    return fig

if __name__ == '__main__':
    fig = main()
    fig_to_d3(fig)

