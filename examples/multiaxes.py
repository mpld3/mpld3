"""
MultiAxes Plot
==============
This example shows how to create a multi-axis plot with tied zoom.

It uses the iris dataset from scikit-learn.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

from mpld3 import show_d3, plugins

data = load_iris()
X = data.data
y = data.target

# dither the data for clearer plotting
X += 0.1 * np.random.random(X.shape)

fig, ax = plt.subplots(4, 4, sharex="col", sharey="row", figsize=(8, 8))
fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95,
                    hspace=0.1, wspace=0.1)

for i in range(4):
    for j in range(4):
        ax[3 - i, j].scatter(X[:, j], X[:, i],
                             c=y, s=40, alpha=0.3)

# remove tick labels
for axi in ax.flat:
    for axis in [axi.xaxis, axi.yaxis]:
        axis.set_major_formatter(plt.NullFormatter())

# add a reset() button
plugins.connect(fig, plugins.ResetButton())

show_d3()
