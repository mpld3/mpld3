"""Plot to test text"""
import matplotlib.pyplot as plt
import mpld3


def create_plot():
    fig, ax = plt.subplots()
    ax.grid(color='gray')

    # test font sizes
    x = 0.1
    for y, size in zip([0.1, 0.3, 0.5, 0.7, 0.9],
                       [8, 12, 16, 20, 24]):
        ax.text(x, y, "size={0}".format(size), size=size, ha='left')

    # test horizontal alignment
    x = 0.5
    for y, align in zip([0.2, 0.4, 0.6],
                        ['left', 'center', 'right']):
        ax.text(x, y, "ha=" + align, ha=align, size=20)

    # test vertical alignment
    y = 0.9
    for x, align in zip([0.5, 0.7, 0.9],
                        ['top', 'center', 'bottom']):
        ax.text(x, y, "va=" + align, ha='center', va=align, size=14)

    # test colors & rotations
    x = 0.8
    for y, c, r in zip([0.15, 0.4, 0.65],
                       ['red', 'blue', 'green'],
                       [-45, 0, 45]):
        ax.text(x, y, "{0} rot={1}".format(c, r),
                size=18, color=c, rotation=r, ha='center', va='center')

    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_title('title', size=20)
    return fig


def test_text():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
