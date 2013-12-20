"""Plot to test polygons"""
import matplotlib.pyplot as plt

def main():
    fig, ax = plt.subplots()
    ax.grid(color='lightgray')

    x = [1, 2, 3, 2, 1, 0, 1]
    y = [0, 0, 1, 2, 2, 1, 0]

    ax.fill(x, y, edgecolor='black', facecolor='lightblue',
            linewidth=3, alpha=0.5)
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 3)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
