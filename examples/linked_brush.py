"""
Linked Brushing Example
=======================
This example shows a prototype of a linked brush plot, using the iris dataset
from scikit-learn.  Eventually, this plugin will be made a part of the mpld3
javascript source.  For now, this should be considered a proof-of-concept.

Click the paintbrush button at the bottom left to enable and disable the
brushing behavior.  The standard zoom and home buttons are available as well.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

import mpld3
from mpld3 import plugins, utils


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
        points = ax[3 - i, j].scatter(X[:, j], X[:, i],
                                      c=y, s=40, alpha=0.6)

# remove tick labels
for axi in ax.flat:
    for axis in [axi.xaxis, axi.yaxis]:
        axis.set_major_formatter(plt.NullFormatter())

plugins.connect(fig, plugins.LinkedBrush(points))

mpld3.show()
