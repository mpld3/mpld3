"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins

fig, ax = plt.subplots()
points = ax.plot(range(10), 'o', ms=20)
plugins.connect(fig, plugins.PointLabelTooltip(points[0],
                                               location="top left"))

mpld3.show()
