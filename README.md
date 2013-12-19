mpld3: A D3 Viewer for Matplotlib
=================================

- Author: Jake Vanderplas <jakevdp@cs.washington.edu>
- License: BSD 3-clause

This is a minimal interactive viewer for matplotlib graphics built on D3.

The code is still very incomplete, and does not (yet) support all of
matplotlib's features.  It should be considered a proof-of-concept, for now.

Installation
------------
To install the library system-wide

    [~]$ python setup.py install

Or, to install locally, use

    [~]$ python setup.py install --prefix=/path/to/location/

Then make sure your Python path points to this location.

Trying it out
-------------
The package is pure python, and very light-weight.  You can take a look at
the notebooks in the examples directory, or run ``create_example.py``, which
will create an output file ``example.html`` which can be viewed in your
browser.

Alternatively, check out the
[IPython notebook examples](http://nbviewer.ipython.org/github/jakevdp/mpld3/tree/master/examples/)
available in the ``examples`` directory.

Features
--------
Currently Supported
~~~~~~~~~~~~~~~~~~~
Currently the support of matplotlib features is very limited.  The code
supports the following:

- multiple axes, placed correctly on the figure
- lines and scatter plots created with ``plt.plot`` (not ``plt.scatter``, etc.)
- grid lines and their properties
- title and axis labels

TODO List
~~~~~~~~~
There are a lot of things which could be implemented fairly easily, given
enough time and energy:

- patches (i.e. shapes like histograms, etc.)
- polygons (filled plots, etc.)
- collections (scatter plots, etc.)
- containers (errorbars, etc.)
- correct text placement and alignment
- log axes and date axes

There are some things that will take a bit more thinking, and be difficult
to do without rethinking some fundamental things

- axes text (i.e. text which pans and zooms with the axis)
- general text formatting

And there are some things which I have no idea how to do well:

- tying together pan/zoom on subplots
- adding a box-zoom tool
- twin axes (i.e. multiple scales on one plot) tied together
- tick specification & formatting

If you have the energy to address any of these, I'd love to accept pull
requests!