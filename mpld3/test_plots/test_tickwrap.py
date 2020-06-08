"""Plot to test date axis"""
import matplotlib.pyplot as plt
import matplotlib
import mpld3


def create_plot():
    labels = [
        "Hey, this is a very long tick label here. I think being long is okay. Just let me be as long as I want to.",
        "I'm actually slightly shorter, but still relatively long.",
        "I'm just doing my thing."
    ]
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.set_title('Tick wrapping test', size=14)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(labels)
    return fig


def test_date():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
