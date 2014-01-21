"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots()
    colors = plt.rcParams['axes.color_cycle']
    points = []                    
    for i, color in enumerate(colors):
        points = ax.plot(i, 0, 'o', c=color)
        plugins.connect(fig,
                        plugins.PointLabelTooltip(points[0], [color]))
    ax.set_xlim(-1, len(colors) + 1)

    return fig

if __name__ == '__main__':
    fig = main()
    fig_to_d3(fig)

