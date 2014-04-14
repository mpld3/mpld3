"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins

fig, ax = plt.subplots()
colors = plt.rcParams['axes.color_cycle']
points = []

for i, color in enumerate(colors):
    points = ax.plot(i, 0, 'o', c=color, ms=20)
    plugins.connect(fig,
                    plugins.PointLabelTooltip(points[0], [color]))
ax.set_xlim(-1, len(colors) + 1)

mpld3.show()
