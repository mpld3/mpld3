"""Plot to test imshow"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots()
    ax.grid(color='gray')

    ax.imshow(np.random.randn(50, 30))

    ax.set_title('An Image', size=20)

    return fig

if __name__ == '__main__':
    main()
    plt.show()
