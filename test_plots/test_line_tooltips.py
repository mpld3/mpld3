"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np

import mpld3
from mpld3 import plugins

fig, ax = plt.subplots()
line, = ax.plot([0, 1, 3, 8, 5], '-', lw=5)
plugins.connect(fig, plugins.LineLabelTooltip(line, ['Line A']))
ax.set_title('Line with Tooltip')

mpld3.show()
