import mpld3
from mpld3.mplexporter import utils
import matplotlib.pylab as plt
import numpy as np
from matplotlib import ticker
from numpy.testing import assert_equal

fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])
ax.set_xlim(0, 1)

def formatter(value, position):
    return f"{position}:{value:.1f}"

ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))

fig.text(0.5, 0.95, 'Global Title', horizontalalignment='center', verticalalignment='top')

props = utils.get_axis_properties(ax.xaxis)

# assert_equal(props['tickformat_formatter'], "fixed")
# assert props['tickvalues'] is not None
# expected = [formatter(value, i)
#             for i, value in enumerate(props['tickvalues'])]
# assert_equal(props['tickformat'], expected)

mpld3.show()
