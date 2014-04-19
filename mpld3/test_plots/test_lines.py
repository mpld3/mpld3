"""Plot to test line styles"""
import matplotlib.pyplot as plt
import mpld3


def create_plot():
    fig, ax = plt.subplots()

    x = [0, 1]

    for i, color in enumerate(['red', 'green', '#0000FF']):
        x = 1 + 6 * i
        for j, alpha in enumerate([0.3, 0.6, 1.0]):
            for k, linestyle in enumerate(['solid', 'dashed',
                                           'dashdot', 'dotted', '--']):
                y = 0.5 + k + 0.33 * j
                lines = ax.plot([x, x + 2.5, x + 5], [y, y + 0.2, y],
                                lw=6 * alpha,
                                c=color, ls=linestyle, alpha=alpha)
                if linestyle == '--':
                    lines[0].set_dashes([8, 4, 2, 4, 2, 4])

    ax.set_ylim(0, 5.5)
    ax.set_title("Line Styles, Widths, Transparencies", size=20)
    return fig


def test_lines():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
