"""
Example Renderer
================
This shows an example of a do-nothing renderer, along with how to use it.
"""
from .base import Renderer


class ExampleRenderer(Renderer):
    def __init__(self):
        self.output = ""

    def open_figure(self, fig, props):
        self.output += "opening figure\n"

    def close_figure(self, fig):
        self.output += "closing figure\n"

    def open_axes(self, ax, props):
        self.output += "  opening axes\n"

    def close_axes(self, ax):
        self.output += "  closing axes\n"

    def draw_line(self, data, coordinates, style, mplobj=None):
        self.output += "    draw line with {0} points\n".format(data.shape[0])

    def draw_markers(self, data, coordinates, style, mplobj=None):
        self.output += "    draw {0} markers\n".format(data.shape[0])
