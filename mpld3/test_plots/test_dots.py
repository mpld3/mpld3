
"""Plot to test legend with dots"""
import matplotlib.pyplot as plt
import mpld3


def create_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='label')
    ax.plot([2, 2, 2], 'o', label='dots')
    ax.set_title(
        'Test legend dots',
        size=14
    )
    ax.legend().set_visible(True)
    return fig


if __name__ == "__main__":
    mpld3.show(create_plot())
