"""
mpld3 Logo Idea
===============
This example shows how mpld3 can be used to generate relatively intricate
vector graphics in the browser. This is an adaptation of a logo proposal by
github user debjan, in turn based on both the matplotlib and D3js logos.
"""
# Author: Jake VanderPlas

import matplotlib.pyplot as plt
from matplotlib import image, patches, colors
from matplotlib.colors import colorConverter
import numpy as np
import mpld3

imsize = np.array([319, 217])
center = [108.5, 108.5]
max_radius = 108.5
radii = np.linspace(16, max_radius, 5)
angles = np.arange(0, 360, 45)


fig = plt.figure(figsize=imsize / 50.)
ax = fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])

# Create a clip path for the elements
clip_path = patches.Rectangle((0, 0), imsize[0], imsize[1],
                              transform=ax.transData)

# Create the background gradient
x = np.array([0, 104, 196, 300])
y = np.linspace(150, 450, 86)[:, None]

c = np.cos(-np.pi / 4)
s = np.sin(-np.pi / 4)
X, Y = (c * x - s * y) - 116, (s * x + c * y)
C = np.arange(255).reshape((3, 85)).T
C = C[::-1, :]
cmap = colors.LinearSegmentedColormap.from_list("mpld3",
                                                [[0.97, 0.6, 0.29],
                                                 [0.97, 0.59, 0.27],
                                                 [0.97, 0.58, 0.25],
                                                 [0.95, 0.44, 0.34],
                                                 [0.92, 0.51, 0.29],
                                                 [0.68, 0.21, 0.20]])
mesh = ax.pcolormesh(X, Y, C, cmap=cmap, shading='auto', zorder=0)
mesh.set_clip_path(clip_path)

# cut-off the background to form the "D" and "3" using white patches
# (this could also be done with a clip path)
kwargs = dict(fc='white', ec='none', zorder=1)
ax.add_patch(patches.Rectangle([0, 0], center[0], imsize[1], **kwargs))

ax.add_patch(patches.Circle(center, radii[2], **kwargs))
ax.add_patch(patches.Wedge(center, 127, -90, 90, width=18.5, **kwargs))

ax.add_patch(patches.Circle((252, 66), 18, **kwargs))
ax.add_patch(patches.Rectangle([216, 48], 36, 36, **kwargs))
ax.add_patch(patches.Wedge((252, 66), 101, -90, 40.1, width=35, **kwargs))

ax.add_patch(patches.Circle((252, 151), 18, **kwargs))
ax.add_patch(patches.Rectangle([216, 133], 36, 36, **kwargs))
ax.add_patch(patches.Wedge((252, 151), 101, -40.1, 90, width=35, **kwargs))

ax.add_patch(patches.Rectangle([-200, -200], 719, 200, **kwargs))
ax.add_patch(patches.Rectangle([-200, -200], 200, 617, **kwargs))
ax.add_patch(patches.Rectangle([-200, imsize[1]], 719, 200, **kwargs))
ax.add_patch(patches.Rectangle([imsize[0], -200], 200, 617, **kwargs))

# plot circles and lines
for radius in radii:
    ax.add_patch(patches.Circle(center, radius, lw=0.5,
                                ec='gray', fc='none', zorder=2))
for angle in angles:
    dx, dy = np.sin(np.radians(angle)), np.cos(np.radians(angle))
    ax.plot([max_radius * (1 - dx), max_radius * (1 + dx)],
            [max_radius * (1 - dy), max_radius * (1 + dy)],
            '-', color='gray', lw=0.5, zorder=2)

# plot wedges within the graph
wedges = [(98, 231, 258, '#FF6600'),
          (85, 170, 205, '#FFC500'),
          (60, 80, 103, '#7DFF78'),
          (96, 45, 58, '#FD7C1A'),
          (73, 291, 308, '#CCFF28'),
          (47, 146, 155, '#28FFCC'),
          (25, 340, 360, '#004AFF')]

for (radius, theta1, theta2, color) in wedges:
    ax.add_patch(patches.Wedge(center, radius, theta1, theta2,
                               fc=color, ec='black', alpha=0.6, zorder=3))

for patch in ax.patches:
    patch.set_clip_path(clip_path)

ax.set_xlim(0, imsize[0])
ax.set_ylim(imsize[1], 0)

#plt.savefig('mpld3.png')
mpld3.show()
