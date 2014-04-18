"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    fig, ax = plt.subplots()

    np.random.seed(0)
    numPoints = 10
    for marker in ['oc', 'vr', '^g', '+k', 'db']:
        ax.plot(np.random.normal(size=numPoints),
                np.random.normal(size=numPoints),
                marker, ms=5+20*np.random.uniform(),
                alpha=0.5*np.random.uniform(),
                mew=1)

    ax.set_xlabel('this is x')
    ax.set_ylabel('this is y')
    ax.set_title('Marker test!', size=14)
    ax.grid(color='lightgray', alpha=0.7)
    return fig


def test_markers():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
