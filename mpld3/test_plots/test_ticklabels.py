"""
Plot to test date axis

TODO (@vladh): This test is misleading and needs to be updated. It should test
dates, but it only plots numbers in [2000, 2050], which will of course get
thousands separators automatically added.
"""
import matplotlib.pyplot as plt
import matplotlib
import mpld3


def create_plot():
    fig, ax = plt.subplots()
    ax.plot([2000, 2050], [1, 2])
    ax.set_title('Tick label test', size=14)
    return fig


def test_date():
    fig = create_plot()
    _ = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
