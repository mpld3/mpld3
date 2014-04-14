"""Plot to test legend"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3

fig, ax = plt.subplots()

x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin', lw=3, alpha=0.5)
ax.plot(x, np.cos(x), label='cos', lw=3, alpha=0.5)
ax.plot(x[::5], 0.5 * np.sin(x[::5] + 2), 'ob', label='dots')

ax.legend(fancybox=True)
ax.set_title("Legend test", size=20)

mpld3.show()
