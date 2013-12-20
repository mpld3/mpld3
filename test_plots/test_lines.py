"""Plot to test line styles"""
import matplotlib.pyplot as plt

def main():
    fig, ax = plt.subplots()
    fig.subplots_adjust(hspace=0.3)

    x = [0, 1]

    for i, color in enumerate(['red', 'green', '#0000FF']):
        for j, alpha in enumerate([0.3, 0.6, 1.0]):
            for k, linestyle in enumerate(['solid', 'dashed',
                                           'dashdot', 'dotted']):
                x = 1 + 6 * i
                y = 0.5 + k + 0.33 * j
                ax.plot([x, x + 2.5, x + 5], [y, y + 0.2, y], lw=6 * alpha,
                        c=color, ls=linestyle, alpha=alpha)

    ax.set_ylim(0, 4.5)
    ax.set_title("Line Styles, Widths, Transparencies", size=20)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
