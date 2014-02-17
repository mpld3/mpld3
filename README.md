mpld3: A D3 Viewer for Matplotlib
=================================

- Author: Jake Vanderplas <jakevdp@cs.washington.edu>
- License: BSD 3-clause

This is an interactive D3js-based viewer which brings matplotlib graphics to the browser.
Please visit [http://mpld3.github.io](http://mpld3.github.io) for documentation and examples.

You may also see the [blog post](http://jakevdp.github.io/blog/2013/12/19/a-d3-viewer-for-matplotlib/), or the
[IPython notebook examples](http://nbviewer.ipython.org/github/jakevdp/mpld3/tree/master/notebooks/)
available in the ``notebooks`` directory of this repository.


Installation
------------
mpld3 requires [jinja2](http://jinja.pocoo.org/) version 2.7+
and [matplotlib](http://matplotlib.org) version 1.3+.

Optionally, mpld3 can be used with [IPython](http://ipython.org), and requires
version 1.1+.

To install the library system-wide, download the source and type

    [~]$ python setup.py install

Or, to install locally, use

    [~]$ python setup.py install --prefix=/path/to/location/

Then make sure your Python path points to this location.

Trying it out
-------------
The package is pure python, and very light-weight.  You can take a look at
the notebooks in the examples directory, or run ``create_example.py``, which
will create a set of plots and launch a browser window showing interactive
views of these plots.

For a more comprehensive set of examples, see the
[IPython notebook examples](http://nbviewer.ipython.org/github/jakevdp/mpld3/tree/master/examples/) available in the ``examples`` directory.

Test Plots
----------
To explore the comparison between D3 renderings and matplotlib renderings for
various plot types, run the script ``process_testplots.py``.  This will generate
an html page with the D3 renderings beside corresponding matplotlib renderings.

Features
--------
### Currently Supported

Currently the support of matplotlib features is very limited.  The code
supports the following:

- multiple axes, placed correctly on the figure
- lines and scatter plots created with ``plt.plot``, ``plt.scatter``, etc.
- grid lines and their properties
- title and axis labels
- patches (i.e. shapes like histograms, etc.)
- polygons (filled plots, etc.)
- some collections (scatter plots, etc.)
- interactive plugins such as tooltips (see http://jakevdp.github.io/blog/2014/01/10/d3-plugins-truly-interactive/)

### TODO List

There are many features still missing, and they range from fairly
straightforward to fairly difficult.

- tick specification & formatting
- some legend features
- twin axes (i.e. multiple scales on one plot) tied together
- additional tools, such as box-zoom

If any of these look like something you'd like to tackle, feel free to submit
a pull request!
