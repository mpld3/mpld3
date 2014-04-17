"""
Plugins to add behavior to mpld3 charts
=======================================

Plugins are means of adding additional javascript features to D3-rendered
matplotlib plots.  A number of plugins are defined here; it is also possible
to create nearly any imaginable behavior by defining your own custom plugin.
"""

__all__ = ['connect', 'clear', 'get_plugins', 'PluginBase',
           'Reset', 'Zoom', 'BoxZoom',
           'PointLabelTooltip', 'PointHTMLTooltip', 'LineLabelTooltip',
           'MousePosition']

import json
import uuid
import matplotlib

from .utils import get_id


def get_plugins(fig):
    """Get the list of plugins in the figure"""
    connect(fig)
    return fig.mpld3_plugins


def connect(fig, *plugins):
    """Connect one or more plugins to a figure

    Parameters
    ----------
    fig : matplotlib Figure instance
        The figure to which the plugins will be connected

    *plugins :
        Additional arguments should be plugins which will be connected
        to the figure.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import plugins
    >>> fig, ax = plt.subplots()
    >>> lines = ax.plot(range(10), '-k')
    >>> plugins.connect(fig, plugins.LineLabelTooltip(lines[0]))
    """
    if not isinstance(fig, matplotlib.figure.Figure):
        raise ValueError("plugins.connect: first argument must be a figure")
    if not hasattr(fig, 'mpld3_plugins'):
        fig.mpld3_plugins = DEFAULT_PLUGINS[:]
    for plugin in plugins:
        fig.mpld3_plugins.append(plugin)


def clear(fig):
    """Clear all plugins from the figure, including defaults"""
    fig.mpld3_plugins = []


class PluginBase(object):
    def get_dict(self):
        return self.dict_

    def javascript(self):
        if hasattr(self, "JAVASCRIPT"):
            if hasattr(self, "js_args_"):
                return self.JAVASCRIPT.render(self.js_args_)
            else:
                return self.JAVASCRIPT
        else:
            return ""

    def css(self):
        if hasattr(self, "css_"):
            return self.css_
        else:
            return ""


class Reset(PluginBase):
    """A Plugin to add a reset button"""
    dict_ = {"type": "reset"}


class MousePosition(PluginBase):
    """A Plugin to display coordinates for the current mouse position

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, plugins.MousePosition())
    >>> fig_to_html(fig)
    """

    def __init__(self, fontsize=12, fmt=".3g"):
        self.dict_ = {"type": "mouseposition",
                      "fontsize": fontsize,
                      "fmt": fmt}


class Zoom(PluginBase):
    """A Plugin to add zoom behavior to the plot

    Parameters
    ----------
    button : boolean, optional
        if True (default), then add a button to enable/disable zoom behavior
    enabled : boolean, optional
        specify whether the zoom should be enabled by default. By default,
        zoom is enabled if button == False, and disabled if button == True.

    Notes
    -----
    Even if ``enabled`` is specified, other plugins may modify this state.
    """
    def __init__(self, button=True, enabled=None):
        if enabled is None:
            enabled = not button
        self.dict_ = {"type": "zoom",
                      "button": button,
                      "enabled": enabled}


class BoxZoom(PluginBase):
    """A Plugin to add box-zoom behavior to the plot

    Parameters
    ----------
    button : boolean, optional
        if True (default), then add a button to enable/disable zoom behavior
    enabled : boolean, optional
        specify whether the zoom should be enabled by default. By default,
        zoom is enabled if button == False, and disabled if button == True.

    Notes
    -----
    Even if ``enabled`` is specified, other plugins may modify this state.
    """
    def __init__(self, button=True, enabled=None):
        if enabled is None:
            enabled = not button
        self.dict_ = {"type": "boxzoom",
                      "button": button,
                      "enabled": enabled}


class PointLabelTooltip(PluginBase):
    """A Plugin to enable a tooltip: text which hovers over points.

    Parameters
    ----------
    points : matplotlib Collection or Line2D object
        The figure element to apply the tooltip to
    labels : array or None
        If supplied, specify the labels for each point in points.  If not
        supplied, the (x, y) values will be used.
    hoffset, voffset : integer
        The number of pixels to offset the tooltip text.  Default is
        hoffset = 0, voffset = 10

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, PointLabelTooltip(points[0]))
    >>> fig_to_html(fig)
    """
    def __init__(self, points, labels=None,
                 hoffset=0, voffset=10, location="mouse"):
        if location not in ["bottom left", "top left", "bottom right",
                            "top right", "mouse"]:
            raise ValueError("invalid location: {0}".format(location))
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "tooltip",
                      "id": get_id(points, suffix),
                      "labels": labels,
                      "hoffset": hoffset,
                      "voffset": voffset,
                      "location": location}


class LineLabelTooltip(PluginBase):
    """A Plugin to enable a tooltip: text which hovers over a line.

    Parameters
    ----------
    line : matplotlib Line2D object
        The figure element to apply the tooltip to
    label : string
        If supplied, specify the labels for each point in points.  If not
        supplied, the (x, y) values will be used.
    hoffset, voffset : integer
        The number of pixels to offset the tooltip text.  Default is
        hoffset = 0, voffset = 10

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, PointLabelTooltip(points[0]))
    >>> fig_to_html(fig)
    """
    def __init__(self, points, label=None,
                 hoffset=0, voffset=10, location="mouse"):
        if location not in ["bottom left", "top left", "bottom right",
                            "top right", "mouse"]:
            raise ValueError("invalid location: {0}".format(location))
        self.dict_ = {"type": "tooltip",
                      "id": get_id(points),
                      "labels": label if label is None else [label],
                      "hoffset": hoffset,
                      "voffset": voffset,
                      "location": location}


class LinkedBrush(PluginBase):
    """A Plugin to enable linked brushing between plots

    Parameters
    ----------
    points : matplotlib Collection or Line2D object
        A representative of the scatter plot elements to brush.
    button : boolean, optional
        if True (default), then add a button to enable/disable zoom behavior
    enabled : boolean, optional
        specify whether the zoom should be enabled by default. default=True.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from mpld3 import fig_to_html, plugins
    >>> X = np.random.random((3, 100))
    >>> fig, ax = plt.subplots(3, 3)
    >>> for i in range(2):
    ...     for j in range(2):
    ...         points = ax[i, j].scatter(X[i], X[j])
    >>> plugins.connect(fig, LinkedBrush(points))
    >>> fig_to_html(fig)

    Notes
    -----
    Notice that in the above example, only one of the four sets of points is
    passed to the plugin. This is all that is needed: for the sake of efficient
    data storage, mpld3 keeps track of which plot objects draw from the same
    data.

    Also note that for the linked brushing to work correctly, the data must
    not contain any NaNs. The presence of NaNs makes the different data views
    have different sizes, so that mpld3 is unable to link the related points.
    """

    def __init__(self, points, button=True, enabled=True):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedbrush",
                      "button": button,
                      "enabled": enabled,
                      "id": get_id(points, suffix)}


class PointHTMLTooltip(PluginBase):
    """A Plugin to enable an HTML tooltip:
    formated text which hovers over points.

    Parameters
    ----------
    points : matplotlib Collection or Line2D object
        The figure element to apply the tooltip to
    labels : list
        The labels for each point in points, as strings of unescaped HTML.
    hoffset, voffset : integer, optional
        The number of pixels to offset the tooltip text.  Default is
        hoffset = 0, voffset = 10
    css : str, optional
        css to be included, for styling the label html if desired
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> labels = ['<h1>{title}</h1>'.format(title=i) for i in range(10)]
    >>> plugins.connect(fig, PointHTMLTooltip(points[0], labels))
    >>> fig_to_html(fig)
    """

    JAVASCRIPT = """
    mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
    HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
    HtmlTooltipPlugin.prototype.requiredProps = ["id"];
    HtmlTooltipPlugin.prototype.defaultProps = {labels:null, hoffset:0, voffset:10};
    function HtmlTooltipPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    HtmlTooltipPlugin.prototype.draw = function(){
       var obj = mpld3.get_element(this.props.id);
       var labels = this.props.labels;
       var tooltip = d3.select("body").append("div")
                    .attr("class", "mpld3-tooltip")
                    .style("position", "absolute")
                    .style("z-index", "10")
                    .style("visibility", "hidden");

       obj.elements()
           .on("mouseover", function(d, i){
                              tooltip.html(labels[i])
                                     .style("visibility", "visible");})
           .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                 }.bind(this))
           .on("mouseout",  function(d, i){
                           tooltip.style("visibility", "hidden");});
    };
    """

    def __init__(self, points, labels=None,
                 hoffset=0, voffset=10, css=None):
        self.points = points
        self.labels = labels
        self.voffset = voffset
        self.hoffset = hoffset
        self.css_ = css or ""
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "htmltooltip",
                      "id": get_id(points, suffix),
                      "labels": labels,
                      "hoffset": hoffset,
                      "voffset": voffset}


DEFAULT_PLUGINS = [Reset(), Zoom(), BoxZoom()]
