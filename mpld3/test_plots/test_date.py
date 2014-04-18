"""Plot to test date axis"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime
import time
import mpld3


def create_plot():
    otimes = [datetime.date(2013, 12, i) for i in range(1, 11)]
    times = matplotlib.dates.date2num(otimes)

    np.random.seed(0)

    fig, ax = plt.subplots()
    ax.xaxis_date()
    fig.autofmt_xdate()
    ax.plot(times, np.random.random(len(times)), "-", linewidth=3)

    return fig


def test_date():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
