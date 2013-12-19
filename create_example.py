import numpy as np
import matplotlib.pyplot as plt
from mpld3 import fig_to_d3

fig, ax = plt.subplots()
ax.plot(np.random.random(10),
        np.random.random(10),
        'og')
ax.plot(np.linspace(0.1, 0.9, 10),
        np.random.random(10), '-b', lw=5, alpha=0.2)
ax.set_xlabel('x label')
ax.set_ylabel('y label')
ax.set_title('title')

filename = "example.html"
print "Writing output to {0}".format(filename)
open(filename, 'w').write(fig_to_d3(fig))
