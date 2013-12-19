import matplotlib.pyplot as plt
from IPython.display import HTML
from . import fig_to_d3


def display_d3(fig, closefig=True):
    if closefig:
        plt.close(fig)
    return HTML(fig_to_d3(fig))
