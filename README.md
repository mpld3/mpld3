mpld3: A D3 Viewer for Matplotlib
=================================

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

Alternatively, check out the IPython notebook examples in the ``examples``
directory.