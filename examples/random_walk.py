"""
Visualizing Random Walks
========================
This shows the use of transparent lines to visualize data.
"""
import numpy as np
import matplotlib.pyplot as plt

N_paths = 50
N_steps = 100

x = np.linspace(0, 10, 100)
y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
y = y.cumsum(1)

ax = plt.axes(xticks=[], yticks=[])
ax.plot(x, y.T, lw=2, c='blue', alpha=0.1)

plt.show()
