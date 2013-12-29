"""Plot to test text"""
import matplotlib.pyplot as plt

def main():
    fig, ax = plt.subplots()
    ax.grid(color='gray')

    # test font sizes
    x = 0.1
    for y, size in zip([0.1, 0.3, 0.5, 0.7, 0.9],
                       [8, 12, 16, 20, 24]):
        ax.text(x, y, "size={0}".format(size), size=size, ha='left')

    # test alignment
    x = 0.5
    for y, align in zip([0.2, 0.4, 0.6],
                        ['left', 'center', 'right']):
        ax.text(x, y, align, ha=align, size=25)

    # test colors
    x = 0.7
    for y, c in zip([0.3, 0.5, 0.7],
                    ['red', 'blue', 'green']):
        ax.text(x, y, c, size=18, color=c)

    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_title('title', size=20)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
