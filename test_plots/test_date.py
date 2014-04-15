"""Plot to test date axis"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime
import time
import mpld3

otimes = [datetime.date(2013, 12, i) for i in range(1, 11)]
times = matplotlib.dates.date2num(otimes)

np.random.seed(0)

fig, ax = plt.subplots()
ax.xaxis_date()
fig.autofmt_xdate()
ax.plot(times, np.random.random(len(times)), "-", linewidth=3)

mpld3.show()
