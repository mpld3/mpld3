"""
Plugins to add behavior to mpld3 charts
"""

__all__ = ['connect', 'PluginBase', 'PointLabelTooltip', 'PointHTMLTooltip',
           'LineLabelTooltip', 'ResetButton']

import jinja2
import json
import uuid

from ._objects import D3Line2D, D3Collection


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
    if not hasattr(fig, 'plugins'):
        fig.plugins = []
    for plugin in plugins:
        fig.plugins.append(plugin)


class PluginBase(object):
    JS = jinja2.Template("")
    FIG_JS = jinja2.Template("")
    HTML = jinja2.Template("")
    STYLE = jinja2.Template("")

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4()).replace('-', '')

    def set_figure(self, figure):
        self.figure = figure

    def _html_args(self):
        return {}

    def html(self):
        return self.HTML.render(self._html_args())

    def _style_args(self):
        return {}

    def style(self):
        return self.STYLE.render(self._style_args())

    def _js_args(self):
        return {}

    def js(self):
        return self.JS.render(self._js_args())

    def _fig_js_args(self):
        return {}

    def fig_js(self):
        return self.FIG_JS.render(self._fig_js_args())

    def _get_d3obj(self, mplobj):
        obj = None
        for ax in self.figure.axes:
            obj = obj or ax.objmap.get(mplobj, None)
        return obj


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
    >>> from mpld3 import fig_to_d3, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, PointLabelTooltip(points[0]))
    >>> fig_to_d3(fig)
    """

    FIG_JS = jinja2.Template("""
    var tooltip{{ id }} = fig.canvas.append("text")
                  .attr("class", "tooltip-text")
                  .attr("x", 0)
                  .attr("y", 0)
                  .text("")
                  .attr("style", "text-anchor: middle;")
                  .style("visibility", "hidden");

    {% if labels != 'null' %}
    var labels{{ id }}  = {{ labels }};
    {% endif %}

    ax{{ axid }}.axes.selectAll(".{{ pointclass }}{{ elid }}")
        .on("mouseover", function(d, i){
                           tooltip{{ id }}
                              .style("visibility", "visible")
                              {% if labels != 'null' %}
                              .text(labels{{ id }} [i])
                              {% else %}
                              .text("(" + d[0] + ", " + d[1] + ")")
                              {% endif %};})
        .on("mousemove", function(d, i){
                          // For some reason, this doesn't work in the notebook
                          // xy = d3.mouse(fig.canvas.node());
                          // use this instead
                          var ctm = fig.canvas.node().getScreenCTM();
                          tooltip{{ id }}
                             .attr('x', d3.event.x - ctm.e - {{ hoffset }})
                             .attr('y', d3.event.y - ctm.f - {{ voffset }});})
        .on("mouseout", function(d, i){tooltip{{ id }}.style("visibility",
                                                             "hidden");});
    """)

    def __init__(self, points, labels=None,
                 hoffset=0, voffset=10):
        self.points = points
        self.labels = labels
        self.voffset = voffset
        self.hoffset = hoffset
        self.id = self.generate_unique_id()

    def _fig_js_args(self):
        obj = self._get_d3obj(self.points)

        if isinstance(obj, D3Line2D):
            pointclass = 'points'
        elif isinstance(obj, D3Collection):
            pointclass = 'paths'
        else:
            raise ValueError("unrecognized object type")

        return dict(id=self.id,
                    hoffset=self.hoffset,
                    voffset=self.voffset,
                    pointclass=pointclass,
                    axid=obj.axid,
                    elid=obj.elcount,
                    labels=json.dumps(self.labels))

class PointHTMLTooltip(PluginBase):
    """A Plugin to enable an HTML tooltip: formated text which hovers over points.

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
    >>> from mpld3 import fig_to_d3, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> labels = ['<h1>{title}</h1>'.format(title=i) for i in range(10)]
    >>> plugins.connect(fig, PointHTMLTooltip(points[0], labels))
    >>> fig_to_d3(fig)
    """

    def __init__(self, points, labels=None,
                 hoffset=0, voffset=10, css=None):
        self.points = points
        self.labels = labels
        self.voffset = voffset
        self.hoffset = hoffset
        self.css = css
        self.id = self.generate_unique_id()

    def _html_args(self):
        return dict(id=self.id,
                    css=self.css)

    HTML = jinja2.Template("""
    <style>
    {{ css }}
    </style>
    """)

    def _fig_js_args(self):
        obj = self._get_d3obj(self.points)

        if isinstance(obj, D3Line2D):
            pointclass = 'points'
        elif isinstance(obj, D3Collection):
            pointclass = 'paths'
        else:
            raise ValueError("unrecognized object type")

        return dict(id=self.id,
                    hoffset=self.hoffset,
                    voffset=self.voffset,
                    pointclass=pointclass,
                    axid=obj.axid,
                    elid=obj.elcount,
                    labels=self.labels)


    FIG_JS = jinja2.Template("""
    var tooltip = d3.select("body").append("div")
                    .attr("class", "mpld3-tooltip")
                    .style("position", "absolute")
                    .style("z-index", "10")
                    .style("visibility", "hidden");

    var labels  = {{ labels }};


    ax{{ axid }}.axes.selectAll(".{{ pointclass }}{{ elid }}")
        .on("mouseover", function(d, i){
                           tooltip
                             .html(labels[i])
                             .style("visibility", "visible");})
        .on("mousemove", function(d, i){
                           tooltip
                             .style("top", (d3.event.pageY+{{ voffset }})+"px")
                             .style("left",(d3.event.pageX+{{ hoffset }})+"px");})
        .on("mouseout",  function(d, i){
                           tooltip
                             .style("visibility", "hidden");});
    """)

class LineLabelTooltip(PluginBase):
    """A Plugin to enable a tooltip: text which hovers over points.

    Parameters
    ----------
    line : matplotlib Line2D object
        The figure element to apply the tooltip to
    label : string
    hoffset, voffset : integer
        The number of pixels to offset the tooltip text.  Default is
        hoffset = 0, voffset = 10

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_d3, plugins
    >>> fig, ax = plt.subplots()
    >>> line, = ax.plot(range(10), '-')
    >>> plugins.connect(fig, LineLabelTooltip(line, 'some label'))
    >>> fig_to_d3(fig)

    To label multiple lines, create multiple LineLabelToopTips.

    >>> fig, ax = plt.subplots()
    >>> x = [0, 1, 2, 3]
    >>> lines = ax.plot(x, [0, 1, 3, 8], x , [5, 7, 1, 2], '-', lw=5)
    >>> labels = ['a', 'b']
    >>> for line, label in zip(lines, labels)
    >>>     plugins.connect(fig, mpld3.plugins.LineLabelTooltip(line, label))
    >>> fig_to_d3(fig)
    """

    FIG_JS = jinja2.Template("""
    var tooltip{{ id }} = fig.canvas.append("text")
                  .attr("class", "tooltip-text")
                  .attr("x", 0)
                  .attr("y", 0)
                  .text("")
                  .attr("style", "text-anchor: middle;")
                  .style("visibility", "hidden");

    ax{{ axid }}.axes.selectAll(".line{{ elid }}")
        .on("mouseover", function(d, i){
                           tooltip{{ id }}
                              .style("visibility", "visible")
                              .text({{label}});})
        .on("mousemove", function(d, i){
                          // For some reason, this doesn't work in the notebook
                          // xy = d3.mouse(fig.canvas.node());
                          // use this instead
                          var ctm = fig.canvas.node().getScreenCTM();
                          tooltip{{ id }}
                             .attr('x', d3.event.x - ctm.e - {{ hoffset }})
                             .attr('y', d3.event.y - ctm.f - {{ voffset }});})
        .on("mouseout", function(d, i){tooltip{{ id }}.style("visibility",
                                                             "hidden");});
    """)

    def __init__(self, line, label,
                 hoffset=0, voffset=10):
        self.line = line
        self.label = label
        self.voffset = voffset
        self.hoffset = hoffset
        self.id = self.generate_unique_id()

    def _fig_js_args(self):
        obj = self._get_d3obj(self.line)

        if not isinstance(obj, D3Line2D):
            raise ValueError("expected Line2D objects")

        return dict(id=self.id,
                    hoffset=self.hoffset,
                    voffset=self.voffset,
                    axid=obj.axid,
                    elid=obj.elcount,
                    label=json.dumps(self.label))


class ResetButton(PluginBase):
    """A Plugin to add a universal reset button

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_d3, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, plugins.ResetButton())
    >>> fig_to_d3(fig)
    """

    FIG_JS = jinja2.Template("""
        fig.root.append("div")
          .append("button")
            .text("Reset")
            .on("click", fig.reset.bind(fig));
    """)

class MousePosition(PluginBase):
    """A Plugin to display coordinates for the current mouse position

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_d3, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> plugins.connect(fig, plugins.MousePosition())
    >>> fig_to_d3(fig)
    """

    FIG_JS = jinja2.Template("""
    var coords = fig.root.append("div")
                   .style("font-family", "monospace");

    for (var i=0; i < fig.axes.length; i++) {
      var update_coords = function() {
            var a = fig.axes[i];  // use function closure to store current axes
            return function() {
              var pos = d3.mouse(this),
                  x = a.x.invert(pos[0]),
                  y = a.y.invert(pos[1]);

              coords.text("Mouse: (" + d3.round(x,4) + ", " + d3.round(y,4) + ")");
            }
          }()
      fig.axes[i].baseaxes
        .on("mousemove", update_coords)
        .on("mouseout", function() {
          coords.text("Mouse:");});
      fig.axes[i].baseaxes.style("cursor", "crosshair");
    }
    """)
