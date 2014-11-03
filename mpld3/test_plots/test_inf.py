"""Plot to test lines with +/-Inf values"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    fig, ax = plt.subplots(nrows=2)

    xx = np.arange(8, dtype=float)
    yy = [-1, 1, -np.inf, 2, -2, np.inf, 1, -1]

    ax[0].plot(xx, yy, 'ks-', ms=10, mec='w', mew=3)
    ax[0].set_xlabel('y includes +/-Inf')
    
    ax[1].semilogy(xx, [1,2,0,1,2,3,4,5], 'ks-', ms=10, mec='w', mew=3)
    ax[1].set_xlabel('y includes 0')
    
    ax[0].set_title('Inf test', size=14)
    return fig

def test_inf():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
