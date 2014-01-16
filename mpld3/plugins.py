"""
Plugins to add behavior to mpld3 charts
"""

__all__ = ['ToolTip']

import jinja2
import json
import uuid

from ._objects import D3Line2D, D3Collection


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
    >>> from mpld3 import fig_to_d3
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> fig.plugins = [PointLabelTooltip(points[0])]
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
                             .attr('x', event.x - ctm.e - {{ hoffset }})
                             .attr('y', event.y - ctm.f - {{ voffset }});})
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
