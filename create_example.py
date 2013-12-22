import os
import urllib2
import numpy as np
import matplotlib.pyplot as plt
from mpld3 import fig_to_d3

# Download d3 file locally
d3_filename = 'd3.v3.min.js'
if not os.path.exists(d3_filename):
    page = urllib2.urlopen('http://d3js.org/d3.v3.min.js')
    with open(d3_filename, 'w') as f:
        f.write(page.read())

# create a plot
fig, ax = plt.subplots(subplot_kw={'axisbg':'#EEEEEE'}, facecolor='white')
ax.plot(np.random.random(10),
        np.random.random(10),
        'ob', markeredgecolor='lightblue',
        markersize=20, markeredgewidth=10, alpha=0.5)
ax.plot(np.linspace(0.1, 0.9, 10),
        np.random.random(10), '-c', lw=5, alpha=0.5)
ax.set_xlabel('x label')
ax.set_ylabel('y label')
ax.set_title('title', fontsize=20)

ax.text(0.2, 0.85, "left", fontsize=18, ha='left')
ax.text(0.2, 0.75, "center", fontsize=18, ha='center')
ax.text(0.2, 0.65, "right", fontsize=18, ha='right')

ax.grid(True, color='white', linestyle='solid')

filename = "example.html"
print "Writing output to {0}".format(filename)
open(filename, 'w').write(fig_to_d3(fig, d3_filename))

#plt.show()
