import random
import json
import jinja2

from ._server import serve_and_open
from .utils import deprecated
from .mplexporter import Exporter
from .mpld3renderer import MPLD3Renderer
from . import urls

__all__ = ["fig_to_html", "fig_to_dict", "fig_to_d3",
           "display_d3", "display",
           "show_d3", "show",
           "enable_notebook", "disable_notebook",
           "save_html", "save_json"]


# Simple HTML template. This works in standalone web pages for single figures,
# but will not work within the IPython notebook due to the presence of
# requirejs
SIMPLE_HTML = jinja2.Template("""
<script type="text/javascript" src="{{ d3_url }}"></script>
<script type="text/javascript" src="{{ mpld3_url }}"></script>

<style>
{{ extra_css }}
</style>

<div id="fig{{ figid }}"></div>
<script type="text/javascript">
  {{ extra_js }}
  var spec{{ figid }} = {{ figure_json }};
  var fig{{ figid }} = mpld3.draw_figure("fig{{ figid }}", spec{{ figid }});
</script>
""")


# RequireJS template.  If requirejs and jquery are not defined, this will
# result in an error.  This is suitable for use within the IPython notebook.
REQUIREJS_HTML = jinja2.Template("""
<style>
{{ extra_css }}
</style>

<div id="fig{{ figid }}"></div>
<script type="text/javascript">
function create_{{ figid }}(){
  {{ extra_js }}
  mpld3.draw_figure("fig{{ figid }}", {{ figure_json }});
}

if(typeof(window.mpld3) === "undefined"){
  require.config({paths: {d3: "{{ d3_url[:-3] }}"}});
  require(["d3"], function(d3){
    window.d3 = d3;
    $.getScript("{{ mpld3_url }}", create_{{ figid }});
  });
}else{
  create_{{ figid }}();
}
</script>
""")


# General HTML template.  This should work correctly whether or not requirejs
# is defined, and whether it's embedded in a notebook or in a standalone
# HTML page.
GENERAL_HTML = jinja2.Template("""
<style>
{{ extra_css }}
</style>

<div id="fig{{ figid }}"></div>
<script>
function mpld3_load_lib(url, callback){
  var s = document.createElement('script');
  s.src = url;
  s.async = true;
  s.onreadystatechange = s.onload = callback;
  s.onerror = function(){console.warn("failed to load library " + url);};
  document.getElementsByTagName("head")[0].appendChild(s);
}

function create_fig{{ figid }}(){
  {{ extra_js }}
  mpld3.draw_figure("fig{{ figid }}", {{ figure_json }});
}

if(typeof(mpld3) !== "undefined"){
   // already loaded: just create the figure
   create_fig{{ figid }}();
}else if(typeof define === "function" && define.amd){
   // require.js is available: use it to load d3/mpld3
   require.config({paths: {d3: "{{ d3_url[:-3] }}"}});
   require(["d3"], function(d3){
      window.d3 = d3;
      mpld3_load_lib("{{ mpld3_url }}", create_fig{{ figid }});
    });
}else{
    // require.js not available: dynamically load d3 & mpld3
    mpld3_load_lib("{{ d3_url }}", function(){
        mpld3_load_lib("{{ mpld3_url }}", create_fig{{ figid }});})
}
</script>
""")

TEMPLATE_DICT = {"simple": SIMPLE_HTML,
                 "notebook": REQUIREJS_HTML,
                 "general": GENERAL_HTML}


def fig_to_dict(fig, d3_url=None, mpld3_url=None,
                template_type="general", **kwargs):
    """Output json representation of the figure

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.
    mpld3_url : string (optional)
        The URL of the mpld3 library.  If not specified, a standard web path
        will be used.
    **kwargs :
        Additional keyword arguments passed to mplexporter.Exporter

    Returns
    -------
    fig_dict : dict
        the Python dictionary representation of the figure, which is
        directly convertible to json using the standard json package.

    See Also
    --------
    - :func:`save_json`: save json representation of a figure to file
    - :func:`save_html` : save html representation of a figure to file
    - :func:`fig_to_html` : output html representation of the figure
    - :func:`show` : launch a local server and show a figure in a browser
    - :func:`display` : embed figure within the IPython notebook
    - :func:`enable_notebook` : automatically embed figures in IPython notebook
    """
    d3_url = d3_url or urls.D3_URL
    mpld3_url = mpld3_url or urls.MPLD3_URL
    figid = str(id(fig)) + str(int(random.random() * 1E10))
    renderer = MPLD3Renderer()
    Exporter(renderer, **kwargs).run(fig)
    fig, figure_json, extra_css, extra_js = renderer.finished_figures[0]
    return figure_json


def fig_to_html(fig, d3_url=None, mpld3_url=None, safemode=False,
                template_type="general", **kwargs):
    """Output html representation of the figure

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display
    d3_url : string (optional)
        The URL of the d3 library.  If not specified, a standard web path
        will be used.
    mpld3_url : string (optional)
        The URL of the mpld3 library.  If not specified, a standard web path
        will be used.
    safemode : boolean
        If true, scrub any additional html
    template_type : string
        string specifying the type of HTML template to use. Options are
        - "simple"   : suitable for a simple html page with one figure.  Will
                       fail if require.js is available on the page.
        - "notebook" : assumes require.js and jquery are available.
        - "general"  : more complicated, but works both in and out of the
                       notebook, whether or not require.js and jquery are
                       available
    **kwargs :
        Additional keyword arguments passed to mplexporter.Exporter

    Returns
    -------
    fig_html : string
        the HTML representation of the figure

    See Also
    --------
    - :func:`save_json`: save json representation of a figure to file
    - :func:`save_html` : save html representation of a figure to file
    - :func:`fig_to_dict` : output dictionary representation of the figure
    - :func:`show` : launch a local server and show a figure in a browser
    - :func:`display` : embed figure within the IPython notebook
    - :func:`enable_notebook` : automatically embed figures in IPython notebook
    """
    template = TEMPLATE_DICT[template_type]

    # TODO: allow fig to be a list of figures?
    d3_url = d3_url or urls.D3_URL
    mpld3_url = mpld3_url or urls.MPLD3_URL
    figid = str(id(fig)) + str(int(random.random() * 1E10))
    renderer = MPLD3Renderer()
    Exporter(renderer, **kwargs).run(fig)

    fig, figure_json, extra_css, extra_js = renderer.finished_figures[0]

    if safemode:
        extra_css = ""
        extra_js = ""

    return template.render(figid=figid,
                           d3_url=d3_url,
                           mpld3_url=mpld3_url,
                           figure_json=json.dumps(figure_json),
                           extra_css=extra_css,
                           extra_js=extra_js)


def display(fig=None, closefig=True, **kwargs):
    """Display figure in IPython notebook via the HTML display hook

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display (grabs current figure if missing)
    closefig : boolean (default: True)
        If true, close the figure so that the IPython matplotlib mode will not
        display the png version of the figure.
    **kwargs :
        additional keyword arguments are passed through to :func:`fig_to_html`.

    Returns
    -------
    fig_d3 : IPython.display.HTML object
        the IPython HTML rich display of the figure.

    See Also
    --------
    - :func:`show` : launch a local server and show a figure in a browser
    - :func:`enable_notebook` : automatically embed figures in IPython notebook
    """
    # import here, in case users don't have requirements installed
    from IPython.display import HTML
    import matplotlib.pyplot as plt
    if fig is None:
        fig = plt.gcf()
    if closefig:
        plt.close(fig)
    return HTML(fig_to_html(fig, **kwargs))


def show(fig=None, ip='127.0.0.1', port=8888, n_retries=50,
         local=True, **kwargs):
    """Open figure in a web browser

    Similar behavior to plt.show().  This opens the D3 visualization of the
    specified figure in the web browser.  On most platforms, the browser
    will open automatically.

    Parameters
    ----------
    fig : matplotlib figure
        The figure to display.  If not specified, the current active figure
        will be used.
    ip : string, default = '127.0.0.1'
        the ip address used for the local server
    port : int, default = 8888
        the port number to use for the local server.  If already in use,
        a nearby open port will be found (see n_retries)
    n_retries : int, default = 50
        the maximum number of ports to try when locating an empty port.
    local : bool, default = True
        if True, use the local d3 & mpld3 javascript versions, within the
        js/ folder.  If False, use the standard urls.
    **kwargs :
        additional keyword arguments are passed through to :func:`fig_to_html`

    See Also
    --------
    - :func:`display` : embed figure within the IPython notebook
    - :func:`enable_notebook` : automatically embed figures in IPython notebook
    """
    if local:
        kwargs['mpld3_url'] = '/mpld3.js'
        kwargs['d3_url'] = '/d3.js'
        files = {'/mpld3.js': ["text/javascript",
                               open(urls.MPLD3_LOCAL, 'r').read()],
                 '/d3.js': ["text/javascript",
                            open(urls.D3_LOCAL, 'r').read()]}
    else:
        files = None

    if fig is None:
        # import here, in case matplotlib.use(...) is called by user
        import matplotlib.pyplot as plt
        fig = plt.gcf()
    html = fig_to_html(fig, **kwargs)
    serve_and_open(html, ip=ip, port=port, n_retries=n_retries, files=files)


def enable_notebook(**kwargs):
    """Enable the automatic display of figures in the IPython Notebook.

    This function should be used with the inline Matplotlib backend
    that ships with IPython that can be enabled with `%pylab inline`
    or `%matplotlib inline`. This works by adding an HTML formatter
    for Figure objects; the existing SVG/PNG formatters will remain
    enabled.

    Parameters
    ----------
    **kwargs :
        all keyword parameters are passed through to :func:`fig_to_html`

    See Also
    --------
    - :func:`disable_notebook` : undo the action of enable_notebook
    - :func:`display` : embed figure within the IPython notebook
    - :func:`show` : launch a local server and show a figure in a browser
    """
    try:
        from IPython.core.getipython import get_ipython
        from matplotlib.figure import Figure
    except ImportError:
        raise ImportError('This feature requires IPython 1.0+ and Matplotlib')
    ip = get_ipython()
    formatter = ip.display_formatter.formatters['text/html']
    formatter.for_type(Figure,
                       lambda fig, kwds=kwargs: fig_to_html(fig, **kwds))


def disable_notebook():
    """Disable the automatic display of figures in the IPython Notebook.

    See Also
    --------
    - :func:`enable_notebook` : automatically embed figures in IPython notebook
    """
    try:
        from IPython.core.getipython import get_ipython
        from matplotlib.figure import Figure
    except ImportError:
        raise ImportError('This feature requires IPython 1.0+ and Matplotlib')
    ip = get_ipython()
    formatter = ip.display_formatter.formatters['text/html']
    formatter.type_printers.pop(Figure, None)


def save_html(fig, fileobj, **kwargs):
    """Save a matplotlib figure to an html file

    Parameters
    ----------
    fig : matplotlib Figure instance
        The figure to write to file.
    fileobj : filename or file object
        The filename or file-like object in which to write the HTML
        representation of the figure.
    **kwargs :
        additional keyword arguments will be passed to :func:`fig_to_html`

    See Also
    --------
    - :func:`save_json`: save json representation of a figure to file
    - :func:`fig_to_html` : output html representation of the figure
    - :func:`fig_to_dict` : output dictionary representation of the figure
    """
    if isinstance(fileobj, str):
        fileobj = open(fileobj, 'w')
    if not hasattr(fileobj, 'write'):
        raise ValueError("fileobj should be a filename or a writable file")
    fileobj.write(fig_to_html(fig, **kwargs))


def save_json(fig, fileobj, **kwargs):
    """Save a matplotlib figure to a json file.
    
    Note that any plugins which depend on generated HTML will not be included
    in the JSON encoding.

    Parameters
    ----------
    fig : matplotlib Figure instance
        The figure to write to file.
    fileobj : filename or file object
        The filename or file-like object in which to write the HTML
        representation of the figure.
    **kwargs :
        additional keyword arguments will be passed to :func:`fig_to_html`

    See Also
    --------
    - :func:`save_html` : save html representation of a figure to file
    - :func:`fig_to_html` : output html representation of the figure
    - :func:`fig_to_dict` : output dictionary representation of the figure
    """
    if isinstance(fileobj, str):
        fileobj = open(fileobj, 'w')
    if not hasattr(fileobj, 'write'):
        raise ValueError("fileobj should be a filename or a writable file")
    json.dump(fig_to_dict(fig, **kwargs), fileobj)


# Deprecated versions of these functions
show_d3 = deprecated(show, "mpld3.show_d3", "mpld3.show")
fig_to_d3 = deprecated(fig_to_html, "mpld3.fig_to_d3", "mpld3.fig_to_html")
display_d3 = deprecated(display, "mpld3.display_d3", "mpld3.display")
