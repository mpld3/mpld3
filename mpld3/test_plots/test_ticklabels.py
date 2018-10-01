"""Plot to test date axis"""
import matplotlib.pyplot as plt
import matplotlib
import mpld3


def create_plot():
    fig, ax = plt.subplots()
    ax.plot([2000,2050], [1,2])
    ax.set_title('Tick label test', size=14)
    return fig


def test_date():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
