import matplotlib
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins


def create_plot():
    fig, ax = plt.subplots()
    ax.plot([1,6], [1,2])
    fmtr = matplotlib.ticker.IndexFormatter(list("ABCDEFG"))
    ax.xaxis.set_major_formatter(fmtr)
    ax.set_title('Tickformat index test', size=14)
    return fig

def test_date():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
