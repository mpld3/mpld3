"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3

fig, ax = plt.subplots()

np.random.seed(0)
numPoints = 10

xx = np.arange(numPoints, dtype=float)
xx[6] = np.nan

yy = np.random.normal(size=numPoints)
yy[3] = np.nan

ax.plot(xx, yy, 'ks-', ms=10, mec='w', mew=3)

ax.set_xlabel('x has uniform spacing')
ax.set_ylabel('y includes a nan')
ax.set_title('NaN test', size=14)

mpld3.show()
