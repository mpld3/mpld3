"""
Zoom Options Example
====================
This example demonstrates a variety of options for zoom-and-pan
behaviors supported by the Zoom plugin.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import mpld3
from mpld3 import plugins, utils

from numpy import inf
x = [3,1,4,1,5,9,2,6,5,3,5,9]
plt.figure(figsize=(8, 3))
plt.plot([3,1,4,1,5,9,2,6,5,3,5,9], 'ks-', ms=10, mew=2, mec='k')

# Here we connect the linked brush plugin
plugins.clear(plt.gcf())
plugins.connect(plt.gcf(), plugins.Reset(), 
                plugins.Zoom(button=True, enabled=True,
                             hover_cursor="-webkit-grab",
                             drag_cursor="-webkit-grabbing",
                             zoom_in_cursor="-webkit-zoom-in",
                             zoom_out_cursor="-webkit-zoom-out",
                             x_offset_limits=[-2,12],
                             x_scale_limits=[.2,5],
                             y_offset_limits=[-1,11],
                             y_scale_limits=[1,1],
                             ))

print mpld3.fig_to_html(plt.gcf(), mpld3_url='/mpld3/js/mpld3.v0.3git.js')
