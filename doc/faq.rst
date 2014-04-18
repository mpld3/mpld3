.. _faq:

Frequently Asked Questions
==========================


General
-------

- **Does mpld3 work for large datasets?**

  Short answer: not really.  Mpld3, like matplolib itself, is designed for small to medium-scale visualizations, and this is unlikely to change. The reason is that mpld3 is built upon the foundation of HTML's SVG, which is not particularly well-suited for large datasets. Plots with more than a few thousand elements will have noticeably slow response for interactive features.

  Big data visualization requires specialized tools which do careful automatic data summarization and/or take direct advantage of your system's GPU. There are a couple other Python projects that are making great headway in this area:

  - `Bokeh <http://bokeh.pydata.org/>`_ is a project which targets browser-based graphics, and recent releases are beginning to do big data in the browser the right way.
  - `VisPy <http://vispy.org>`_ is another effort to provide easy visualization of large datasets. It is based on OpenGL, with plans to add a WebGL backend.

- **What matplotlib features are not supported?**

  matplotlib is a complicated system, and there are lots of small corner cases that are difficult to render correctly in d3. mpld3 correctly handles a large majority of matplotlib plots, but some pieces remain unsupported either because they have not yet been implemented, or because there are fundamental difficulties preventing their inclusion.

  We keep a list of unsupported features at https://github.com/jakevdp/mpld3/wiki#mpld3-missing-features.  If you find something missing that's not on that list, please feel free to add it.

- **Can I use mpld3 without matplotlib?**

  Yes! The client-side interface of mpld3 is a pure javascript library, which builds figures based on a well-defined JSON specification. This specification was designed with matplotlib in mind, but there's nothing stopping you from generating the JSON from another source, or even editing it by hand. Unfortunately, at the moment, this JSON spec is not well-documented, but we hope to address that in the future.


IPython Notebook
----------------

- **Why does IPython notebook freeze when I run an mpld3 example?**

  Short answer: This most often happens when someone uses :func:`mpld3.show` within the IPython notebook. Use :func:`mpld3.display` or :func:`mpld3.enable_notebook` when using mpld3 with IPython notebook. See the :ref:`quickstart-guide` for a description of the various mpld3 functions.

  Long answer: like matplotlib's :func:`plt.show` function, :func:`mpld3.show` does not play well with the IPython notebook. :func:`mpld3.show` generates an html representation of a figure, then launches a local web server and attempts to open a browser page to display it. This behavior is nice when running a stand-alone script, but is generally not what you want within the IPython notebook, which is already in a browser window!

- **Why am I getting strange javascript errors within the iPython notebook?**

  Most likely, the notebook contains multiple versions of the mpld3 javascript source. Javascript has a way of hanging around in the IPython notebook even when you don't want it to. The first step in this situation is the following:

  1. Clear all the output in the notebook (This can be done via the toolbar, with Cell -> All Output -> Clear)
  2. Save your notebook
  3. Close the notebook window
  4. Re-open the notebook window

  You now have a clean notebook, and can try running an mpld3 script again.

- **I'm using SSL to have a secure connection and/or make a remote IPython notebook play nice with Windows 8. How do I get mpld3 to work?**

  Default browser security settings do not allow secure web pages to load javascript libraries from an insecure server. To work around this, simply specify alternative urls for d3 and mpld3 when you call :func:`mpld3.enable_notebook`. For example::

    mpld3.enable_notebook(d3_url='//mpld3.github.io/js/d3.v3.min.js',
                          mpld3_url='//mpld3.github.io/js/mpld3.v0.1.js')


Javascript
----------

- **Where is the mpld3 javascript library located?**

  There is a local copy of the mpld3 library bundled with the package, which you can find in ``mpld3/js/mpld3.v0.2.js`` where ``v0.2`` indicates the library version, and matches the version of the mpld3 Python package. This local copy is used with the command ``mpld3.show``, so that no internet connection is needed. Online copies of the library can be found at, e.g. http://mpld3.github.io/js/mpld3.v0.2.js. This is automatically used within the IPython notebook, and commands like :func:`mpld3.save_html`, :func:`mpld3.fig_to_html`, etc.

- **How can I use mpld3 without an internet connection?**

  To use mpld3 without an internet connection, you need to use a local version of the mpld3 and d3 libraries. Outside the IPython notebook, you can use the :func:`mpld3.show()` function, which automatically uses local copies of the javascript libraries.

  Inside the IPython notebook, both the :func:`mpld3.enable_notebook` and :func:`mpld3.display` functions take a boolean keyword ``local``. Setting this to ``True`` will copy the mpld3 and d3 javascript libraries to the notebook directory, and will use the appropriate path within IPython (``/files/*.js``) to load the libraries.
