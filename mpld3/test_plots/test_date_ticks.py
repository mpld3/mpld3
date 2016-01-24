"""Plot to test custom date axis tick locations and labels"""
from datetime import datetime
import matplotlib.pyplot as plt
import mpld3

def create_plot():
    times = [datetime(2013, 12, i) for i in range(1,9)]
    ticks = [times[2],times[3],times[-2]]
    labels = [t.strftime("%Y-%m-%d") for t in ticks]

    plt.plot_date(times, times, xdate=True, ydate=True)
    plt.xticks(ticks,labels)
    plt.yticks(ticks)

    return plt.gcf()


def test_date():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot(),template_type='simple')
