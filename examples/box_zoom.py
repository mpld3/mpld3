import mpld3
from mpld3.plugins import BoxZoom

import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(2, 2, sharex='col', sharey='row')

for i in range(2):
    for j in range(2):
        ax[i, j].plot(np.random.normal(0, 1, 100),
                      np.random.normal(0, 1, 100),
                      'ok', alpha=0.3)

mpld3.plugins.connect(fig, BoxZoom())
mpld3.show()
