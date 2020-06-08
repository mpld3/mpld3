"""
Plot to test custom date axis tick locations and labels

NOTE (@vladh): We may see different behaviour in mpl vs d3 for the y axis, because we never
specified exactly how we want the y axis formatted. This is ok.
"""
from datetime import datetime
import matplotlib.pyplot as plt
import mpld3


def create_plot():
    times = [datetime(2013, 12, i) for i in range(1, 20)]
    ticks = [times[0], times[1], times[2], times[6], times[-2], times[-1]]
    labels = [t.strftime("%Y-%m-%d") for t in ticks]

    plt.plot_date(times, times, xdate=True, ydate=True)
    plt.xticks(ticks, labels)
    plt.yticks(ticks)
    plt.xlim([times[1], times[-2]])
    plt.ylim([times[1], times[-2]])

    return plt.gcf()


def test_date():
    fig = create_plot()
    _ = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot(), template_type='simple')
