mpld3: A D3 Viewer for Matplotlib
=================================

- Maintainers: [@cliffckerr](https://github.com/cliffckerr) and [@vladh](https://github.com/vladh)
- Author: Jake Vanderplas <jakevdp@cs.washington.edu>
- License: BSD 3-clause

This is an interactive D3js-based viewer which brings matplotlib graphics to the browser.
Please visit [http://mpld3.github.io](http://mpld3.github.io) for documentation and examples.

You may also see the [blog post](http://jakevdp.github.io/blog/2013/12/19/a-d3-viewer-for-matplotlib/), or the
[IPython notebook examples](http://nbviewer.ipython.org/github/jakevdp/mpld3/tree/master/notebooks/)
available in the ``notebooks`` directory of this repository.

[![version status](https://img.shields.io/pypi/v/mpld3.svg)](https://pypi.python.org/pypi/mpld3)
[![downloads](https://img.shields.io/pypi/dm/mpld3.svg)](https://pypi.python.org/pypi/mpld3)
[![build status](https://travis-ci.org/jakevdp/mpld3.svg?branch=master)](https://travis-ci.org/jakevdp/mpld3)


About
-----
mpld3 provides a custom stand-alone javascript library built on D3, which
parses JSON representations of plots.  The mpld3 python module provides a
set of routines which parses matplotlib plots (using the 
[mplexporter](http://github.com/mpld3/mplexporter) framework) and outputs
the JSON description readable by mpld3.js.


Installation
------------
mpld3 is compatible with python 2.6-2.7 and 3.3-3.4. It requires
[matplotlib](http://matplotlib.org) version 2.2.2 and
[jinja2](http://jinja.pocoo.org/) version 2.7+.

Optionally, mpld3 can be used with [IPython](http://ipython.org) notebook,
and requires IPython version 1.x or (preferably) version 2.0+.

This package is based on the [mplexporter](http://github.com/mpld3/mplexporter)
framework for crawling and exporting matplotlib images. mplexporter is bundled
with the source distribution via git submodule.

Within the git source directory, you can download the mplexporter dependency
and copy it into the mpld3 source directory using the following command:

    [~]$ python setup.py submodule

The submodule command is not necessary if you are installing from a distribution
rather than from the git source.

Once the submodule command has been run, you can build the package locally using

    [~]$ python setup.py build

or install the package to the standard Python path using:

    [~]$ python setup.py install

Or, to install to another location, use

    [~]$ python setup.py install --prefix=/path/to/location/

Then make sure your PYTHONPATH environment variable points to this location.

Trying it out
-------------
The package is pure python, and very light-weight.  You can take a look at
the notebooks in the examples directory, or run ``create_example.py``, which
will create a set of plots and launch a browser window showing interactive
views of these plots.

For a more comprehensive set of examples, see the
[IPython notebook examples](http://nbviewer.ipython.org/github/jakevdp/mpld3/tree/master/notebooks/) available in the ``notebooks`` directory.

Test Plots
----------
To explore the comparison between D3 renderings and matplotlib renderings for
various plot types, run the script ``visualize_tests.py``.  This will generate
an HTML page with the D3 renderings beside corresponding matplotlib renderings.

Features
--------
Many of the core features of matplotlib are already supported.  And additionally
there is some extra interactivity provided via the plugin framework.  The
following is a non-exhausive list of features that are yet to be supported:

- tick specification & formatting
- some legend features
- blended transforms, such as those required by ``axvlines`` and ``axhlines``
- twin axes (i.e. multiple scales on one plot) tied together

If any of these look like something you'd like to tackle, feel free to submit
a pull request!
