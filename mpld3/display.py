import matplotlib.pyplot as plt
from IPython.display import HTML
from .fig_to_d3 import fig_to_d3, D3_LOAD


def display_d3(fig, closefig=True):
    if closefig:
        plt.close(fig)
    return HTML(fig_to_d3(fig, load_d3=False))

def load_d3():
    return HTML(D3_LOAD)
