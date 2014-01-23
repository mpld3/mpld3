"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, fig_to_d3

def main():
    fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
    N = 100

    scatter = ax.scatter(np.random.normal(size=N),
                         np.random.normal(size=N),
                         c=np.random.random(size=N),
                         s = 1000 * np.random.random(size=N),
                         alpha=0.3,
                         cmap=plt.cm.jet)
    ax.grid(color='white', linestyle='solid')

    ax.set_title("Scatter Plot (with tooltips!)", size=20)

    labels = ['point {0}'.format(i + 1) for i in range(N)]
    tooltip = plugins.PointLabelTooltip(scatter, labels=labels)
    plugins.connect(fig, tooltip)

    return fig

if __name__ == '__main__':
    fig = main()
    fig_to_d3(fig)

