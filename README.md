mpld3: A D3 Viewer for Matplotlib
=================================

- Author: Jake Vanderplas <jakevdp@cs.washington.edu>
- License: BSD 3-clause

This is an interactive D3js-based viewer which brings matplotlib graphics to the browser.
Please visit [http://mpld3.github.io](http://mpld3.github.io) for documentation and examples.

You may also see the [blog post](http://jakevdp.github.io/blog/2013/12/19/a-d3-viewer-for-matplotlib/), or the
[IPython notebook examples](http://nbviewer.ipython.org/github/jakevdp/mpld3/tree/master/notebooks/)
available in the ``notebooks`` directory of this repository.


About
-----
mpld3 provides a custom stand-alone javascript library built on D3, which
parses JSON representations of plots.  The mpld3 python module provides a
set of routines which parses matplotlib plots (using the 
[mplexporter](http://github.com/mpld3/mplexporter) framework) and outputs
the JSON description readable by mpld3.js.


Installation
------------
mpld3 requires [jinja2](http://jinja.pocoo.org/) version 2.7+
and [matplotlib](http://matplotlib.org) version 1.3+.
This package is based on the [mplexporter](http://github.com/mpld3/mplexporter)
framework for crawling and exporting matplotlib images. mplexporter is bundled
with the source distribution via git submodule.

Optionally, mpld3 can be used with [IPython](http://ipython.org), and requires
version 1.1+.

To download the mplexporter dependency and bundle it into the mpld3 package, run

    [~]$ make build

To install the package via setup.py, type 

    [~]$ make install

Or, to install locally, after running ``make build`` use

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
Many of the core features of matplotlib are already supported.  And additionally
there is some extra interactivity provided via the plugin framework.  The
following is a non-exhausive list of features that are yet to be supported:

- tick specification & formatting
- some legend features
- blended transforms, such as those required by ``axvlines`` and ``axhlines``
- twin axes (i.e. multiple scales on one plot) tied together
- additional interactivity tools, such as brushing and box-zoom.

If any of these look like something you'd like to tackle, feel free to submit
a pull request!
