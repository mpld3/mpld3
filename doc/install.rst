.. _installing-mpld3:

Installing mpld3
================

Installing released versions
----------------------------
The mpld3 project is compatible with Python 2.6-2.7 and 3.3-3.4.
To install the latest release, you can use the `pip installer <http://www.pip-installer.org/>`_ as follows::

    [~]$ pip install mpld3

If you've downloaded the tarball of the source distribution, you can type::

    [~]$ python setup.py install

or to specify another install location, use::

    [~]$ python setup.py install --prefix=/path/to/location/

Installing from git
-------------------
The mpld3 source is `available on GitHub <http://github.com/jakevdp/mpld3>`_.
Installing from source requires one extra build step to sync the `mplexporter <http://github.com/mpld3/mplexporter>`_ submodule.
When installing from the gihub source, use::

    [~]$ python setup.py submodule
    [~]$ python setup.py install

Building JavaScript Sources
---------------------------
A core piece of the mpld3 package are the JavaScript libraries, which are located in the package in the ``mpld3/js/`` directory.
The ``mpld3.*.js`` is automatically constructed from a number of source JavaScript files; if you modify these sources, the libraries must be re-built before mpld3 is installed. For more information, please refer to ``CONTRIBUTING.md``, found in the project repository.

Dependencies
------------
The mpld3 package is compatible with Python versions 2.6, 2.7, 3.3, and 3.4.
It requires `matplotlib <http://matplotlib.org>`_ version 1.3+ and `jinja2 <http://jinja.pocoo.org>`_ version 2.7+.
Optionally, mpld3 can be used within the `IPython <http://ipython.org>`_ notebook, and requires IPython version 1.0+, and preferably IPython 2.0+ (see notes in the documentation of :func:`mpld3.enable_notebook`).
