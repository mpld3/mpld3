"""
Image with labels derived from mouse position
=============================================

This example shows how mpld3 can display arbitrary labels derived from
the coordinates of the mouse position.  The coordinates of the mouse
position are rounded down to the nearest integer and used as indices
into arrays `xlabels` and `ylabels`.  One use-case is to draw a
heatmap of a matrix as an image, and display labels for the rows and
columns of the matrix.
"""
import matplotlib.pyplot as plt
import numpy as np

import mpld3
from mpld3 import plugins

fig, ax = plt.subplots()
mat = np.random.normal(size=(6, 4))

xlabels = ["Column %s" % x for x in "ABCD"]
ylabels = ["Row %d" % j for j in range(6)]

im = ax.imshow(mat, aspect='auto', interpolation='nearest')
fig.colorbar(im, ax=ax)

plugins.connect(fig, plugins.MousePositionLabels(xlabels, ylabels, fontsize=14))

mpld3.show()
