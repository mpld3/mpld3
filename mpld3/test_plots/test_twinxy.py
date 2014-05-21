"""Plot to test twinx"""
import numpy as np
import matplotlib.pyplot as plt
import mpld3


def create_plot():
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    
    # twinx test
    t = np.arange(0.01, 10.0, 0.01)
    s1 = np.exp(t)
    ax1.plot(t, s1, 'b-')

    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('original data', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    s2 = np.sin(2*np.pi*t)
    ax2.plot(t, s2, 'r.')
    ax2.set_ylabel('twin', color='r')
    ax2.xaxis.tick_top()
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    
    #twiny test   
    ax3 = fig.add_subplot(2, 1, 2)
    ax3.plot(t, s2)
    
    ax4 = ax3.twiny()
    t2 = np.arange(0.01, 20, 0.02)
    s3 = np.sin(2*np.pi*t2)
    ax4.plot(t2, s3, 'r.')
    ax4.yaxis.tick_right()

    return fig


def test_twinx():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
