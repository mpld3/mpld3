"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots()
    line, = ax.plot([0, 1, 3, 8, 5], '-', lw=5)
    plugins.connect(fig, plugins.LineLabelTooltip(line, 'Line A'))
    ax.set_title('Line with Tooltip')

    return fig

if __name__ == '__main__':
    fig = main()
    fig_to_d3(fig)

