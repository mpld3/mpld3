"""Plot to test date axis"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime
import time

def main():
    otimes = map(datetime.datetime.fromtimestamp, [time.time()+i*500
                                                   for i in range(10)])
    times = matplotlib.dates.date2num(otimes)

    fig, ax = plt.subplots()
    ax.xaxis_date()
    fig.autofmt_xdate()
    ax.plot_date(times, range(10),"-",linewidth=3)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
