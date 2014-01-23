"""Plot to test line styles"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import fig_to_d3

def main():
    fig, ax = plt.subplots()
    points = ax.plot(range(10), 'o', color='none', mec='k')
    return fig

if __name__ == '__main__':
    fig = main()
    fig_to_d3(fig)

