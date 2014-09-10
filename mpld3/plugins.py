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

import collections
import json
import uuid
import matplotlib
from numpy import inf

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
    hover_cursor : str, optional
    drag_cursor  : str, optional
    zoom_in_cursor : str, optional
    zoom_out_cursor : str, optional
        cursor css property for corresponding interaction
    x_scale_limits, y_scale_limits : list-like, optional
        minimum and maximum values for scale factor when zooming.  Use
        (1,1) to disable zoom.
    x_offset_limits, y_offset_limits : like-like, optional
        minimum and maximum values for panning.

    Notes
    -----
    Even if ``enabled`` is specified, other plugins may modify this state.
    """
    def __init__(self, button=True, enabled=None,
                 hover_cursor="move", drag_cursor="move",
                 zoom_in_cursor="move", zoom_out_cursor="move",
                 x_scale_limits=(0,inf), x_offset_limits=(-inf,inf),
                 y_scale_limits=(0,inf), y_offset_limits=(-inf,inf)):
        if enabled is None:
            enabled = not button
        self.dict_ = locals()
        self.dict_.pop('self')
            

        self.dict_["type"] = "zoom"

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
    >>> lines = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, LineLabelTooltip(lines[0]))
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
    HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                hoffset:0,
                                                voffset:10};
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


class LineHTMLTooltip(PluginBase):
    """A Plugin to enable an HTML tooltip:
    formated text which hovers over points.

    Parameters
    ----------
    points : matplotlib Line2D object
        The figure element to apply the tooltip to
    label : string
        The label for the line, as strings of unescaped HTML.
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
    >>> lines = ax.plot(range(10))
    >>> label = '<h1>line {title}</h1>'.format(title='A')
    >>> plugins.connect(fig, LineHTMLTooltip(lines[0], label))
    >>> fig_to_html(fig)
    """

    JAVASCRIPT = """
    mpld3.register_plugin("linehtmltooltip", LineHTMLTooltip);
    LineHTMLTooltip.prototype = Object.create(mpld3.Plugin.prototype);
    LineHTMLTooltip.prototype.constructor = LineHTMLTooltip;
    LineHTMLTooltip.prototype.requiredProps = ["id"];
    LineHTMLTooltip.prototype.defaultProps = {label:null,
                                              hoffset:0,
                                              voffset:10};
    function LineHTMLTooltip(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LineHTMLTooltip.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id, this.fig);
        var label = this.props.label
        var tooltip = d3.select("body").append("div")
                    .attr("class", "mpld3-tooltip")
                    .style("position", "absolute")
                    .style("z-index", "10")
                    .style("visibility", "hidden");

        obj.elements()
           .on("mouseover", function(d, i){
                               tooltip.html(label)
                                      .style("visibility", "visible");
                                     })
            .on("mousemove", function(d, i){
                  tooltip
                    .style("top", d3.event.pageY + this.props.voffset + "px")
                    .style("left",d3.event.pageX + this.props.hoffset + "px");
                 }.bind(this))
           .on("mouseout",  function(d, i){
                           tooltip.style("visibility", "hidden");})
    };
    """

    def __init__(self, line, label=None,
                 hoffset=0, voffset=10,
                 css=None):
        self.line = line
        self.label = label
        self.voffset = voffset
        self.hoffset = hoffset
        self.css_ = css or ""
        self.dict_ = {"type": "linehtmltooltip",
                      "id": get_id(line),
                      "label": label,
                      "hoffset": hoffset,
                      "voffset": voffset}


class InteractiveLegendPlugin(PluginBase):
    """A plugin for an interactive legends.

    Inspired by http://bl.ocks.org/simzou/6439398

    Parameters
    ----------
    plot_elements : iterable of matplotlib elements
        the elements to associate with a given legend items
    labels : iterable of strings
        The labels for each legend element
    ax :  matplotlib axes instance, optional
        the ax to which the legend belongs. Default is the first
        axes. The legend will be plotted to the right of the specified
        axes
    alpha_sel : float, optional
        the alpha value to apply to the plot_element(s) associated
        with the legend item when the legend item is selected.
        Default is 1.0
    alpha_unsel : float, optional
        the alpha value to apply to the plot_element(s) associated
        with the legend item when the legend item is unselected.
        Default is 0.2
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> N_paths = 5
    >>> N_steps = 100
    >>> x = np.linspace(0, 10, 100)
    >>> y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
    >>> y = y.cumsum(1)
    >>> fig, ax = plt.subplots()
    >>> labels = ["a", "b", "c", "d", "e"]
    >>> line_collections = ax.plot(x, y.T, lw=4, alpha=0.1)
    >>> interactive_legend = plugins.InteractiveLegendPlugin(line_collections,
    ...                                                      labels,
    ...                                                      alpha_unsel=0.1)
    >>> plugins.connect(fig, interactive_legend)
    >>> fig_to_html(fig)
    """

    JAVASCRIPT = """
    mpld3.register_plugin("interactive_legend", InteractiveLegend);
    InteractiveLegend.prototype = Object.create(mpld3.Plugin.prototype);
    InteractiveLegend.prototype.constructor = InteractiveLegend;
    InteractiveLegend.prototype.requiredProps = ["element_ids", "labels"];
    InteractiveLegend.prototype.defaultProps = {"ax":null,
                                                "alpha_sel":1.0,
                                                "alpha_unsel":0}
    function InteractiveLegend(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    InteractiveLegend.prototype.draw = function(){
        var alpha_sel = this.props.alpha_sel;
        var alpha_unsel = this.props.alpha_unsel;

        var legendItems = new Array();
        for(var i=0; i<this.props.labels.length; i++){
            var obj = {};
            obj.label = this.props.labels[i];

            var element_id = this.props.element_ids[i];
            mpld3_elements = [];
            for(var j=0; j<element_id.length; j++){
                var mpld3_element = mpld3.get_element(element_id[j], this.fig);

                // mpld3_element might be null in case of Line2D instances
                // for we pass the id for both the line and the markers. Either
                // one might not exist on the D3 side
                if(mpld3_element){
                    mpld3_elements.push(mpld3_element);
                }
            }

            obj.mpld3_elements = mpld3_elements;
            obj.visible = false; // should become be setable from python side
            legendItems.push(obj);
        }

        // determine the axes with which this legend is associated
        var ax = this.props.ax
        if(!ax){
            ax = this.fig.axes[0];
        } else{
            ax = mpld3.get_element(ax, this.fig);
        }

        // add a legend group to the canvas of the figure
        var legend = this.fig.canvas.append("svg:g")
                               .attr("class", "legend");

        // add the rectangles
        legend.selectAll("rect")
                .data(legendItems)
             .enter().append("rect")
                .attr("height",10)
                .attr("width", 25)
                .attr("x",ax.width+10+ax.position[0])
                .attr("y",function(d,i) {
                            return ax.position[1]+ i * 25 - 10;})
                .attr("stroke", get_color)
                .attr("class", "legend-box")
                .style("fill", function(d, i) {
                            return d.visible ? get_color(d) : "white";})
                .on("click", click);

        // add the labels
        legend.selectAll("text")
                .data(legendItems)
            .enter().append("text")
              .attr("x", function (d) {
                            return ax.width+10+ax.position[0] + 40;})
              .attr("y", function(d,i) {
                            return ax.position[1]+ i * 25;})
              .text(function(d) { return d.label });

        // specify the action on click
        function click(d,i){
            d.visible = !d.visible;
            d3.select(this)
              .style("fill",function(d, i) {
                return d.visible ? get_color(d) : "white";
              })

            for(var i=0; i<d.mpld3_elements.length; i++){
                var type = d.mpld3_elements[i].constructor.name;
                if(type =="mpld3_Line"){
                    d3.select(d.mpld3_elements[i].path[0][0])
                        .style("stroke-opacity",
                                d.visible ? alpha_sel : alpha_unsel);
                } else if((type=="mpld3_PathCollection")||
                         (type=="mpld3_Markers")){
                    d3.selectAll(d.mpld3_elements[i].pathsobj[0])
                        .style("stroke-opacity",
                                d.visible ? alpha_sel : alpha_unsel)
                        .style("fill-opacity",
                                d.visible ? alpha_sel : alpha_unsel);
                } else{
                    console.log(type + " not yet supported");
                }
            }
        };

        // helper function for determining the color of the rectangles
        function get_color(d){
            var type = d.mpld3_elements[0].constructor.name;
            var color = "black";
            if(type =="mpld3_Line"){
                color = d.mpld3_elements[0].props.edgecolor;
            } else if((type=="mpld3_PathCollection")||
                      (type=="mpld3_Markers")){
                color = d.mpld3_elements[0].props.facecolors[0];
            } else{
                console.log(type + " not yet supported");
            }
            return color;
        };
    };
    """

    css_ = """
    .legend-box {
      cursor: pointer;
    }
    """

    def __init__(self, plot_elements, labels, ax=None,
                 alpha_sel=1, alpha_unsel=0.2):

        self.ax = ax

        if ax:
            ax = get_id(ax)

        mpld3_element_ids = self._determine_mpld3ids(plot_elements)
        self.mpld3_element_ids = mpld3_element_ids
        self.dict_ = {"type": "interactive_legend",
                      "element_ids": mpld3_element_ids,
                      "labels": labels,
                      "ax": ax,
                      "alpha_sel": alpha_sel,
                      "alpha_unsel": alpha_unsel}

    def _determine_mpld3ids(self, plot_elements):
        """
        Helper function to get the mpld3_id for each
        of the specified elements.
        """
        mpld3_element_ids = []

        # There are two things being done here. First,
        # we make sure that we have a list of lists, where
        # each inner list is associated with a single legend
        # item. Second, in case of Line2D object we pass
        # the id for both the marker and the line.
        # on the javascript side we filter out the nulls in
        # case either the line or the marker has no equivalent
        # D3 representation.
        for entry in plot_elements:
            ids = []
            if isinstance(entry, collections.Iterable):
                for element in entry:
                    mpld3_id = get_id(element)
                    ids.append(mpld3_id)
                    if isinstance(element, matplotlib.lines.Line2D):
                        mpld3_id = get_id(element, 'pts')
                        ids.append(mpld3_id)
            else:
                ids.append(get_id(entry))
                if isinstance(entry, matplotlib.lines.Line2D):
                    mpld3_id = get_id(entry, 'pts')
                    ids.append(mpld3_id)
            mpld3_element_ids.append(ids)

        return mpld3_element_ids

DEFAULT_PLUGINS = [Reset(), Zoom(), BoxZoom()]
