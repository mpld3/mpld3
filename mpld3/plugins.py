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
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

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
    targets : list
        The urls that each point will open when clicked.
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
                                                target:null,
                                                hoffset:0,
                                                voffset:10,
                                                targets:null};
    function HtmlTooltipPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    HtmlTooltipPlugin.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        var labels = this.props.labels;
        var targets = this.props.targets;
        var tooltip = d3.select("body").append("div")
            .attr("class", "mpld3-tooltip")
            .style("position", "absolute")
            .style("z-index", "10")
            .style("visibility", "hidden");

        obj.elements()
            .on("mouseover", function(d, i){
                tooltip.html(labels[i])
                    .style("visibility", "visible");
            })
            .on("mousemove", function(d, i){
                tooltip
                .style("top", d3.event.pageY + this.props.voffset + "px")
                .style("left",d3.event.pageX + this.props.hoffset + "px");
            }.bind(this))
            .on("mousedown.callout", function(d, i){
                window.open(targets[i],"_blank");
            })
            .on("mouseout", function(d, i){
                tooltip.style("visibility", "hidden");
            });
    };
    """

    def __init__(self, points, labels=None, targets=None,
                 hoffset=0, voffset=10, css=None):
        self.points = points
        self.labels = labels
        self.targets = targets
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
                      "targets": targets,
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
    alpha_unsel : float, optional
        the alpha value to multiply the plot_element(s) associated alpha
        with the legend item when the legend item is unselected.
        Default is 0.2
    alpha_over : float, optional
        the alpha value to multiply the plot_element(s) associated alpha
        with the legend item when the legend item is overlaid.
        Default is 1 (no effect), 1.5 works nicely !
    start_visible : boolean, optional (could be a list of booleans)
        defines if objects should start selected on not.
    font_size : int, optional
        defines legend font-size.
        Default is 10.
    legend_offset : list of int (length: 2)
        defines horizontal offset and vertical offset of legend.
        Default is (0, 0).

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
    >>> line_collections = ax.plot(x, y.T, lw=4, alpha=0.6)
    >>> interactive_legend = plugins.InteractiveLegendPlugin(line_collections,
    ...                                                      labels,
    ...                                                      alpha_unsel=0.2,
    ...                                                      alpha_over=1.5,
    ...                                                      start_visible=True,
    ...                                                      font_size=14,
    ...                                                      legend_offset=(-100,20))
    >>> plugins.connect(fig, interactive_legend)
    >>> fig_to_html(fig)
    """

    JAVASCRIPT = """
    mpld3.register_plugin("interactive_legend", InteractiveLegend);
    InteractiveLegend.prototype = Object.create(mpld3.Plugin.prototype);
    InteractiveLegend.prototype.constructor = InteractiveLegend;
    InteractiveLegend.prototype.requiredProps = ["element_ids", "labels"];
    InteractiveLegend.prototype.defaultProps = {"ax":null,
                                                "alpha_unsel":0.2,
                                                "alpha_over":1.0,
                                                "start_visible":true,
                                                "font_size": 10,
                                                "legend_offset": [0,0]}
    function InteractiveLegend(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    InteractiveLegend.prototype.draw = function(){
        var alpha_unsel = this.props.alpha_unsel;
        var alpha_over = this.props.alpha_over;
        var font_size = this.props.font_size;
        var legend_offset = this.props.legend_offset;

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
            obj.visible = this.props.start_visible[i]; // should become be setable from python side
            legendItems.push(obj);
            set_alphas(obj, false);
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
                .attr("height", 0.7*font_size)
                .attr("width", 1.6*font_size)
                .attr("x", ax.width + ax.position[0] + 15 + legend_offset[0])
                .attr("y",function(d,i) {
                           return ax.position[1] + i * (font_size+5) + 10 + legend_offset[1];})
                .attr("stroke", get_color)
                .attr("class", "legend-box")
                .style("fill", function(d, i) {
                           return d.visible ? get_color(d) : "white";})
                .on("click", click).on('mouseover', over).on('mouseout', out);

        // add the labels
        legend.selectAll("text")
              .data(legendItems)
              .enter().append("text")
              .attr("font-size", font_size)
              .attr("x", function (d) {
                           return ax.width + ax.position[0] + (1.9*font_size+15) + legend_offset[0];})
              .attr("y", function(d,i) {
                           return ax.position[1] + i * (font_size+5) + 10 + (0.72*font_size-1) + legend_offset[1];})
              .text(function(d) { return d.label })
              .on('mouseover', over).on('mouseout', out);


        // specify the action on click
        function click(d,i){
            d.visible = !d.visible;
            d3.select(this)
              .style("fill",function(d, i) {
                return d.visible ? get_color(d) : "white";
              })
            set_alphas(d, false);

        };

        // specify the action on legend overlay 
        function over(d,i){
             set_alphas(d, true);
        };

        // specify the action on legend overlay 
        function out(d,i){
             set_alphas(d, false);
        };

        // helper function for setting alphas
        function set_alphas(d, is_over){
            for(var i=0; i<d.mpld3_elements.length; i++){
                var type = d.mpld3_elements[i].constructor.name;

                if(type =="mpld3_Line"){
                    var current_alpha = d.mpld3_elements[i].props.alpha;
                    var current_alpha_unsel = current_alpha * alpha_unsel;
                    var current_alpha_over = current_alpha * alpha_over;
                    d3.select(d.mpld3_elements[i].path.nodes()[0])
                        .style("stroke-opacity", is_over ? current_alpha_over :
                                                (d.visible ? current_alpha : current_alpha_unsel))
                        .style("stroke-width", is_over ?
                                alpha_over * d.mpld3_elements[i].props.edgewidth : d.mpld3_elements[i].props.edgewidth);
                } else if((type=="mpld3_PathCollection")||
                         (type=="mpld3_Markers")){
                    var current_alpha = d.mpld3_elements[i].props.alphas[0];
                    var current_alpha_unsel = current_alpha * alpha_unsel;
                    var current_alpha_over = current_alpha * alpha_over;
                    d.mpld3_elements[i].pathsobj
                        .style("stroke-opacity", is_over ? current_alpha_over :
                                                (d.visible ? current_alpha : current_alpha_unsel))
                        .style("fill-opacity", is_over ? current_alpha_over :
                                                (d.visible ? current_alpha : current_alpha_unsel));
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
                 alpha_unsel=0.2, alpha_over=1., start_visible=True, font_size=10, legend_offset=(0,0)):

        self.ax = ax

        if ax:
            ax = get_id(ax)

        # start_visible could be a list
        if isinstance(start_visible, bool):
            start_visible = [start_visible] * len(labels)
        elif not len(start_visible) == len(labels):
            raise ValueError("{} out of {} visible params has been set"
                             .format(len(start_visible), len(labels)))     

        mpld3_element_ids = self._determine_mpld3ids(plot_elements)
        self.mpld3_element_ids = mpld3_element_ids
        self.dict_ = {"type": "interactive_legend",
                      "element_ids": mpld3_element_ids,
                      "labels": labels,
                      "ax": ax,
                      "alpha_unsel": alpha_unsel,
                      "alpha_over": alpha_over,
                      "start_visible": start_visible,
                      "font_size": font_size,
                      "legend_offset": legend_offset}

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
            if isinstance(entry, Iterable):
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


class PointClickableHTMLTooltip(PluginBase):
    """A plugin for pop-up windows with data with rich HTML

    Parameters
    ----------
    points : matplotlib Collection object
        The figure element to apply the tooltip to
    labels : list
        The labels for each point in points, as strings of unescaped HTML.
    targets : list
        The target data or rich HTML to be displayed when each collection element is clicked
    hoffset, voffset : integer, optional
        The number of pixels to offset the tooltip text.  Default is
        hoffset = 0, voffset = 10
    css : str, optional
        css to be included, for styling the label html and target data/tables, if desired
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import plugins
    >>> fig, ax = plt.subplots(1,1)
    >>> xx = yy = range(10)
    >>> scat = ax.scatter(xx, range(10))
    >>> targets = map(lambda (x, y): "<marquee>It works!<br><h1>{}, {}</h1></marquee>".format(x, y),
    >>>               zip(xx, yy))
    >>> labels = map(lambda (x, y): "{}, {}".format(x,y), zip(xx, yy))
    >>> from mpld3.plugins import PointClickableHTMLTooltip
    >>> plugins.connect(fig, PointClickableHTMLTooltip(scat, labels=labels, targets=targets))

    """

    JAVASCRIPT="""
    mpld3.register_plugin("clickablehtmltooltip", PointClickableHTMLTooltip);
    PointClickableHTMLTooltip.prototype = Object.create(mpld3.Plugin.prototype);
    PointClickableHTMLTooltip.prototype.constructor = PointClickableHTMLTooltip;
    PointClickableHTMLTooltip.prototype.requiredProps = ["id"];
    PointClickableHTMLTooltip.prototype.defaultProps = {labels:null,
                                                 targets:null,
                                                 hoffset:0,
                                                 voffset:10};
    function PointClickableHTMLTooltip(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    PointClickableHTMLTooltip.prototype.draw = function(){
       var obj = mpld3.get_element(this.props.id);
       var labels = this.props.labels;
       var targets = this.props.targets;

       var tooltip = d3.select("body").append("div")
                    .attr("class", "mpld3-tooltip")
                    .style("position", "absolute")
                    .style("z-index", "10")
                    .style("visibility", "hidden");

       obj.elements()
           .on("mouseover", function(d, i){
                  if ($(obj.elements()[0][0]).css( "fill-opacity" ) > 0 || $(obj.elements()[0][0]).css( "stroke-opacity" ) > 0) {
                              tooltip.html(labels[i])
                                     .style("visibility", "visible");
                              } })

           .on("mousedown", function(d, i){
                              window.open().document.write(targets[i]);
                               })
           .on("mousemove", function(d, i){
                  tooltip
                    .style("top", d3.event.pageY + this.props.voffset + "px")
                    .style("left",d3.event.pageX + this.props.hoffset + "px");
                 }.bind(this))
           .on("mouseout",  function(d, i){
                           tooltip.style("visibility", "hidden");});
    };
    """
    def __init__(self, points, labels=None, targets=None,
                 hoffset=2, voffset=-6, css=None):
        self.points = points
        self.labels = labels
        self.targets = targets
        self.voffset = voffset
        self.hoffset = hoffset
        self.css_ = css or ""
        if targets is not None:
            styled_targets = map(lambda x: self.css_ + x, targets)
        else:
            styled_targets = None


        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "clickablehtmltooltip",
                      "id": get_id(points, suffix),
                      "labels": labels,
                      "targets": styled_targets,
                      "hoffset": hoffset,
                      "voffset": voffset}


class MouseXPosition(PluginBase):
    """Like MousePosition, but only show the X coordinate"""

    JAVASCRIPT="""
  mpld3.register_plugin("mousexposition", MouseXPositionPlugin);
  MouseXPositionPlugin.prototype = Object.create(mpld3.Plugin.prototype);
  MouseXPositionPlugin.prototype.constructor = MouseXPositionPlugin;
  MouseXPositionPlugin.prototype.requiredProps = [];
  MouseXPositionPlugin.prototype.defaultProps = {
    fontsize: 12,
    fmt: "0d"
  };
  function MouseXPositionPlugin(fig, props) {
    mpld3.Plugin.call(this, fig, props);
  }
  MouseXPositionPlugin.prototype.draw = function() {
    var fig = this.fig;
    var fmt = d3.format(this.props.fmt);
    var coords = fig.canvas.append("text").attr("class", "mpld3-coordinates").style("text-anchor", "end").style("font-size", this.props.fontsize).attr("x", this.fig.width - 5).attr("y", this.fig.height - 5);
    for (var i = 0; i < this.fig.axes.length; i++) {
      var update_coords = function() {
        var ax = fig.axes[i];
        return function() {
          var pos = d3.mouse(this), x = ax.x.invert(pos[0]), y = ax.y.invert(pos[1]);
          coords.text(fmt(x));
        };
      }();
      fig.axes[i].baseaxes.on("mousemove", update_coords).on("mouseout", function() {
        coords.text("");
      });
    }
  };"""
    """A Plugin to display coordinates for the current mouse position

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, plugins.MouseXPosition())
    >>> fig_to_html(fig)
    """

    def __init__(self, fontsize=12, fmt="8.0f"):
        self.dict_ = {"type": "mousexposition",
                      "fontsize": fontsize,
                      "fmt": fmt}

DEFAULT_PLUGINS = [Reset(), Zoom(), BoxZoom()]
