.. _quickstart-guide:

Quick Start Guide
=================

.. currentmodule:: mpld3

The mpld3 package is extremely easy to use: you can simply take any script
generating a matplotlib plot, run it through one of mpld3's convenience
routines, and embed the result in a web page. For some example of this
in action, see the :ref:`example-gallery`.  Here we'll give a quick overview
of the basic mpld3 functions you should know about.


General Functions
-----------------

:func:`fig_to_d3`
    This is the core routine which takes a figure and constructs a string of
    html and javascript which can be embedded in any webpage.

:func:`show_d3`
    This function is mpld3's equivalent of matplotlib's ``plt.show`` function.
    It will convert the current figure to html, start a local webserver which
    serves this html, and (if the operating system allows it) automatically
    open this page in the web browser.


IPython Notebook Functions
--------------------------

:func:`display_d3`
    This function displays a single mpld3 figure inline within the IPython
    notebook. It is useful if you want to use the standard static figure
    display hook through the notebook, but override it in a few cases.
    If you want every matplotlib figure to be displayed via mpld3, use
    the :func:`enable_notebook` function, described below.

:func:`enable_notebook`
    This function will adjust the IPython notebook display properties so that
    mpld3 will be used to display every figure, without having to call
    :func:`display_d3`. This is useful if you want every figure to be
    automatically embedded in the notebook as an interactive javascript figure.
    Note: this should be used in conjunction with the ``%matplotlib inline``
    mode within the notebook: see the `IPython documentation
    <http://ipython.org/ipython-doc/dev/interactive/notebook.html#plotting>`_
    for details.

:func:`disable_notebook`
    This function undoes the changes made by :func:`enable_notebook`, so that
    the normal matplotlib backend is used instead.


Plugins
-------
Plugins are a way to extend matplotlib figures with interactive features that
will appear in the browser-based visualization.  There are several examples
of these plugins in the :ref:`example-gallery`.  For some examples of built-in
plugins, see :ref:`scatter_tooltip` and :ref:`html_tooltips`.  For some
examples of defining custom plugin behavior, see :ref:`random_walk` and
:ref:`custom_plugin`.
