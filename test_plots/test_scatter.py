"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
    N = 100

    ax.scatter(np.random.normal(size=N),
               np.random.normal(size=N),
               c=np.random.random(size=N),
               s = 1000 * np.random.random(size=N),
               alpha=0.3,
               cmap=plt.cm.jet)
    ax.grid(color='white', linestyle='solid')

    ax.set_title("Scatter Plot", size=20)
    return fig

if __name__ == '__main__':
    main()
    plt.show()
