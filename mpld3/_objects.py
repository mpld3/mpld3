import abc
import uuid
import warnings
import base64
import io
import json
from textwrap import dedent
from collections import defaultdict

import jinja2

import numpy as np

import matplotlib.axis
from matplotlib.lines import Line2D
from matplotlib.image import imsave
from matplotlib.path import Path
from matplotlib.text import Text
from matplotlib.patches import Patch
from matplotlib import ticker
import matplotlib as mpl
from matplotlib.transforms import Affine2D
from matplotlib.markers import MarkerStyle

from ._utils import (color_to_hex, get_dasharray, path_data, collection_data)
from . import _js as js


D3_URL = "http://d3js.org/d3.v3.min.js"


class D3Base(object):
    """Abstract Base Class for D3js objects"""
    __metaclass__ = abc.ABCMeta

    # keep track of the number of children of each element:
    # this assists in generating unique ids for all HTML elements
    num_children_by_id = defaultdict(int)

    HTML = jinja2.Template("")
    STYLE = jinja2.Template("")

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4()).replace('-', '')

    def _initialize(self, parent=None, obj=None, **kwds):
        # set attributes
        self.parent = parent
        self.obj = obj
        for key, val in kwds.items():
            setattr(self, key, val)

        # create various identifiers for the object
        if parent is None:
            self.elcount = 1
        else:
            self.num_children_by_id[self.parent.elid] += 1
            self.elcount = self.num_children_by_id[self.parent.elid]

        self.elname = self.__class__.__name__.lower()
        if self.elname.startswith('d3'):
            self.elname = self.elname[2:]

        self.var = self.elname + str(self.elcount)
        self.cssclass = self.elname + str(self.elcount)
        self.elid = self.generate_unique_id()
        self.cssid = self.elname + self.elid

    @property
    def zorder(self):
        if hasattr(self.obj, 'zorder'):
            return self.obj.zorder
        else:
            return 0

    @property
    def axvar(self):
        """The JS variable used to store the axes object"""
        return "ax{0}".format(self.axid)

    def __getattr__(self, attr):
        if attr in ['fig', 'ax', 'figid', 'axid', 'figcssid']:
            if hasattr(self, '_' + attr):
                return getattr(self, '_' + attr)
            elif self.parent is not None and self.parent is not self:
                return getattr(self.parent, attr)
        else:
            raise AttributeError("no attribute {0}".format(attr))

    def _base_args(self):
        return {'figid': self.figid,
                'figcssid': self.figcssid,
                'axid': self.axid,
                'axvar': self.axvar,
                'elid': self.elid,
                'cssid': self.cssid,
                'cssclass': self.cssclass,
                'var': self.var,
                'fig': self.fig,
                'ax': self.ax,
                'obj': self}

    def _html_args(self):
        return {}

    def _style_args(self):
        return {}

    def html(self):
        argdict = self._base_args()
        argdict.update(self._html_args())
        return dedent(self.HTML.render(**argdict))

    def style(self):
        argdict = self._base_args()
        argdict.update(self._style_args())
        return dedent(self.STYLE.render(**argdict))

    def __str__(self):
        return self.html()


class D3Figure(D3Base):
    """Class for representing a matplotlib Figure in D3js"""

    HTML = jinja2.Template("""
    {% if standalone %}<!DOCTYPE html>
    <html>
    <head>
      {% if title %}
        <title>{{ title }}</title>
      {% endif %}
    {% endif %}
    {% if with_js_includes %}
    {% if extra_js %}{{ extra_js }}{% endif %}
    {% endif %}
    {% if with_style %}
    <style>
      {% for ax in axes %}
        {{ ax.style() }}
      {% endfor %}
    {% if extra_style %}{{ extra_style }}{% endif %}
    </style>
    {% endif %}
    {% if standalone %}
    </head>
    <body>
    {% endif %}
    {% if with_body %}
    <div id='figure{{ figid }}'>
    </div>
    <script type="text/javascript">
    var create_fig{{ figid }} = function(d3, undefined){
      {% for function in js_functions %}
        {{ function }}
      {% endfor %}
      var figwidth = {{ fig.get_figwidth() }} * {{ fig.dpi }};
      var figheight = {{ fig.get_figheight() }} * {{ fig.dpi }};
      var fig = new Figure("div#figure{{ figid }}",
                           figwidth, figheight);

      {% for ax in axes %}
         {{ ax.html() }}
      {% endfor %}

      {% for ax in axes %}
       {% if ax.sharex %}
        {{ ax.axvar }}.sharex = [{{ ax.sharex|join(', ') }}];
       {% endif %}
       {% if ax.sharey %}
        {{ ax.axvar }}.sharey = [{{ ax.sharey|join(' ,') }}];
       {% endif %}
      {% endfor %}

      fig.draw();

      {% if extra_fig_js %}{{ extra_fig_js }}{% endif %}

      return fig
    }

    // set a timeout of 0: this makes things work in the IPython notebook
    setTimeout(function(){
      // we need to call the function, making sure d3 is defined appropriately
      if(typeof define === "function" && define.amd){
        // If require.js is available, use it to load d3
        require.config({paths: {d3: "{{ d3_url[:-3] }}"}});
        require(["d3"], create_fig{{ figid }});
      }else if(typeof d3 === "undefined"){
        // No require.js: dynamically load d3
        var s = document.createElement('script');
        s.src = "{{ d3_url }}";
        s.async = true;
        s.onreadystatechange = s.onload = s.onerror = function() {
           if(typeof d3 === "undefined"){
              document.getElementById("figure{{ figid }}").innerHTML =
                    "<p style='color:red;'>(d3 failed to load)</p>";
           }else{
              create_fig{{ figid }}(d3);
           }
        };
        document.getElementsByTagName("head")[0].appendChild(s);
      }else{
        // d3 is already globally loaded
        create_fig{{ figid }}(d3);
      }
    }, 0);

    </script>
    {% if extra_body %}{{ extra_body }}{% endif %}
    {% endif %}
    {% if standalone %}
    </body>
    </html>
    {% endif %}
    """)

    def __init__(self, fig):
        self._initialize(parent=None, obj=fig)
        self._figid = self.elid
        self._figcssid = "figure" + self._figid
        self._fig = fig
        self._ax = None
        self.axes = [D3Axes(self, ax) for ax in fig.axes]

        self.sharex = []
        self.sharey = []

        # figure out shared axes groups
        for i, ax in enumerate(self.axes):
            #TODO: what about shared axes between figures?
            xsib = ax.ax.get_shared_x_axes().get_siblings(ax.ax)
            ysib = ax.ax.get_shared_y_axes().get_siblings(ax.ax)

            ax.sharex = [axi.axvar for axi in self.axes
                         if axi is not ax and axi.ax in xsib]
            ax.sharey = [axi.axvar for axi in self.axes
                         if axi is not ax and axi.ax in ysib]

    def style(self, **kwargs):
        """Return the style tags for the figure."""
        return self._render(with_body=False,
                            with_js_includes=False,
                            **kwargs)

    def js_includes(self, **kwargs):
        """Return the javascript includes for the figure."""
        return self._render(with_body=False,
                            with_style=False,
                            **kwargs)

    def body(self, **kwargs):
        """Return the body content for the figure."""
        return self._render(with_js_includes=False,
                            with_style=False,
                            **kwargs)

    def html(self, d3_url=None, **kwargs):
        """Output HTML representing the figure."""
        return self._render(d3_url, **kwargs)

    def _render(self, d3_url=None,
                standalone=False, title=None,
                with_js_includes=True, extra_js=None,
                with_style=True, extra_style=None,
                with_body=True, extra_body=None,
                extra_fig_js=None):
        """Render the figure (or parts of the figure) as d3."""
        # here we call savefig so that draw() commands will happen
        # use fig.dpi, otherwise rcparams savefig() can override this
        self.fig.savefig(io.BytesIO(), format='png', dpi=self.fig.dpi)

        # now write the html
        if hasattr(self.fig, 'plugins'):
            if not extra_js:
                extra_js = ''

            if not extra_style:
                extra_style = ''

            if not extra_body:
                extra_body = ''

            if not extra_fig_js:
                extra_fig_js = ''

            for plugin in self.fig.plugins:
                plugin.set_figure(self)
                extra_js += plugin.js()
                extra_style += plugin.style()
                extra_body += plugin.html()
                extra_fig_js += plugin.fig_js()

        if d3_url is None:
            d3_url = D3_URL
        return dedent(self.HTML.render(figid=self.figid,
                                       fig=self.fig,
                                       axes=self.axes,
                                       d3_url=d3_url,
                                       js_functions=js.ALL_FUNCTIONS,
                                       with_js_includes=with_js_includes,
                                       extra_js=extra_js,
                                       extra_fig_js=extra_fig_js,
                                       with_style=with_style,
                                       extra_style=extra_style,
                                       with_body=with_body,
                                       extra_body=extra_body,
                                       title=title))


class D3Axes(D3Base):
    """Class for representing a matplotlib Axes in D3js"""

    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    .axesbg{
        fill: {{ axesbg }};
    }

    {% for child in children %}
      {{ child.style() }}
    {% endfor %}
    """)

    HTML = jinja2.Template("""
    var {{ axvar }} = new Axes(fig, {{ bbox }}, {{ xlim }}, {{ ylim }},
                               {{ xscale }}, {{ yscale }},
                               {{ xdomain }}, {{ ydomain }},
                               {{ xgrid }}, {{ ygrid }},
                               "axes{{ axid }}",
                               "clip{{ figid }}{{ axid }}", {{ zoomable }});

    {% for child in children %}
      {{ child.html() }}
    {% endfor %}
    """)

    def __init__(self, parent, ax):
        self._initialize(parent=parent, obj=ax, _ax=ax)
        self._axid = self.elcount
        self.sharedx = []
        self.sharedy = []
        self.children = []
        self.objmap = {}

        # Note that the order of the children is the order of their stacking
        # on the page: we append things we want on top (like text) last.

        # TODO: re-order children according to their zorder.
        self._add_children(D3Axis(self, self.ax.xaxis),
                           D3Axis(self, self.ax.yaxis))

        self._add_children(*[D3Image(self, image) for image in ax.images])

        if self.has_xgrid():
            self._add_children(D3Grid(self, ax.xaxis))
        if self.has_ygrid():
            self._add_children(D3Grid(self, ax.yaxis))

        self._add_children(*[D3Line2D(self, line) for line in ax.lines])
        self._add_children(*[D3Patch(self, patch)
                             for i, patch in enumerate(ax.patches)])

        for collection in ax.collections:
            if isinstance(collection, mpl.collections.PolyCollection):
                self._add_children(D3PatchCollection(self, collection))
            elif isinstance(collection, mpl.collections.LineCollection):
                self._add_children(D3LineCollection(self, collection))
            elif isinstance(collection, mpl.collections.QuadMesh):
                self._add_children(D3QuadMesh(self, collection))
            elif isinstance(collection, mpl.collections.PathCollection):
                self._add_children(D3PathCollection(self, collection))
            else:
                warnings.warn("{0} not implemented.  "
                              "Elements will be ignored".format(collection))

        for artist in ax.artists:
            if isinstance(artist, Text):
                self._add_children(D3Text(self, artist))
            else:
                warnings.warn("artist {0} not implemented. "
                              "Elements will be ignored".format(artist))

        self._add_children(*[D3Text(self, text) for text in ax.texts])
        self._add_children(*[D3Text(self, text) for text in [ax.xaxis.label,
                                                             ax.yaxis.label,
                                                             ax.title]])

        # Some warnings for pieces of matplotlib which are not yet implemented
        if len(ax.tables) > 0:
            warnings.warn("tables not implemented. Elements will be ignored")

        # re-order children according to their zorder.
        self.children.sort(key=lambda child: child.zorder)

        # draw legend on top
        if ax.legend_ is not None:
            for child in ax.legend_.get_children()[:-1]:
                if isinstance(child, Patch):
                    self._add_children(D3Patch(self, child))

            for child in ax.legend_.get_children():
                if isinstance(child, Text):
                    # legend usually contains text with 'None': why?
                    if not (child is ax.legend_.get_children()[-1]
                            and child.get_text() == 'None'):
                        self._add_children(D3Text(self, child))
                elif isinstance(child, Patch):
                    pass
                elif isinstance(child, Line2D):
                    self._add_children(D3Line2D(self, child))
                else:
                    warnings.warn("Ignoring legend element: {0}".format(child))

    def _add_children(self, *children):
        for child in children:
            self.children.append(child)
            self.objmap[child.obj] = child

    def has_xgrid(self):
        return bool(self.ax.xaxis._gridOnMajor
                    and self.ax.xaxis.get_gridlines())

    def has_ygrid(self):
        return bool(self.ax.yaxis._gridOnMajor
                    and self.ax.yaxis.get_gridlines())

    def _style_args(self):
        return dict(axesbg=color_to_hex(self.ax.patch.get_facecolor()),
                    children=self.children)

    def zoomable(self):
        return bool(self.ax.get_navigate())

    def _html_args(self):
        args = dict(bbox=json.dumps(self.ax.get_position().bounds),
                    xgrid=json.dumps(self.has_xgrid()),
                    ygrid=json.dumps(self.has_ygrid()),
                    children=self.children,
                    zoomable=json.dumps(self.zoomable()))

        # get args for each axis
        for axname in ['x', 'y']:
            axis = getattr(self.ax, axname + 'axis')
            domain = getattr(self.ax, 'get_{0}lim'.format(axname))()
            lim = json.dumps(domain)
            if isinstance(axis.converter, mpl.dates.DateConverter):
                scale = 'date'
                domain = ["new Date{0}".format((d.year, d.month - 1, d.day,
                                                d.hour, d.minute, d.second,
                                                d.microsecond * 1E-3))
                          for d in mpl.dates.num2date(domain)]
                domain = "[{0}]".format(",".join(domain))
            else:
                scale = axis.get_scale()
                domain = json.dumps(domain)

            if scale not in ['date', 'linear', 'log']:
                raise ValueError("Unknown axis scale: "
                                 "{0}".format(axis[axname].get_scale()))

            args[axname + 'scale'] = json.dumps(scale)
            args[axname + 'lim'] = lim
            args[axname + 'domain'] = domain

        return args


class D3Axis(D3Base):
    """Class for representing x/y-axis in D3js"""

    HTML = jinja2.Template("""
    // Add an Axis element
    {{ axvar }}.add_element(new Axis({{ axvar }}, {{ position }},
                                     {{ nticks }}, {{ tickvalues }},
                                     {{ tickformat }}));
    """)

    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    .axis line, .axis path {
        shape-rendering: crispEdges;
        stroke: black;
        fill: none;
    }

    div#figure{{ figid }}
    .axis text {
        font-family: sans-serif;
        font-size: {{ fontsize }}px;
        fill: black;
        stroke: none;
    }
    """)

    def __init__(self, parent, axis):
        self._initialize(parent=parent, obj=axis, axis=axis)
        self.position = self.axis.get_ticks_position()

        # TODO: allow labels/ticks to be drawn on both sides
        # TODO: make sure grid lines line-up with ticks
        label1On = self.axis._major_tick_kw.get('label1On', True)

        if isinstance(self.axis, matplotlib.axis.XAxis):
            if label1On:
                self.position = "bottom"
            else:
                self.position = "top"
            self.lim = self.ax.get_xlim()
            self.labels = self.ax.get_xticklabels()
        elif isinstance(self.axis, matplotlib.axis.YAxis):
            if label1On:
                self.position = "left"
            else:
                self.position = "right"
            self.lim = self.ax.get_ylim()
            self.labels = self.ax.get_yticklabels()
        else:
            raise ValueError("{0} should be an Axis instance".format(axis))

    def get_nticks(self):
        # TODO: handle locations more specifically.  The current solution is
        #       sufficient for NullLocator, MaxNLocator, and FixedLocator,
        #       but not as well for AutoLocator, MultipleLocator, and others.
        locator = self.axis.get_major_locator()
        return len(locator())

    def get_tickvalues(self):
        locator = self.axis.get_major_locator()
        if isinstance(locator, ticker.FixedLocator):
            # override nticks
            return json.dumps(list(locator()))
        else:
            # null indicates that nticks should be used.
            return json.dumps(None)

    def get_tickformat(self):
        # TODO: handle formats other than Null
        formatter = self.axis.get_major_formatter()
        if isinstance(formatter, ticker.NullFormatter):
            return json.dumps("")
        elif not any(label.get_visible() for label in self.labels):
            return json.dumps("")
        else:
            return json.dumps(None)

    def _html_args(self):
        return {'position': json.dumps(self.position),
                'nticks': self.get_nticks(),
                'tickvalues': self.get_tickvalues(),
                'tickformat': self.get_tickformat()}

    def _style_args(self):
        ticks = self.axis.get_ticklabels()

        if len(ticks) == 0:
            fontsize = 11
        else:
            fontsize = ticks[0].properties()['size']

        return {'fontsize': fontsize}


class D3Grid(D3Base):
    """Class for representing axes grids in D3js"""

    HTML = jinja2.Template("""
    // Add a Grid element
    {{ axvar }}.add_element(new Grid({{ axvar }}, {{ grid_type }}));
    """)

    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    .grid .tick {
      stroke: {{ color }};
      stroke-dasharray: {{ dasharray }};
      stroke-opacity: {{ alpha }};
    }

    div#figure{{ figid }}
    .grid path {
      stroke-width: 0;
    }
    """)

    def __init__(self, parent, axis):
        if isinstance(axis, matplotlib.axis.XAxis):
            grid_type = "x"
        elif isinstance(axis, matplotlib.axis.YAxis):
            grid_type = "y"
        else:
            raise ValueError("grid argument must be an x or y axis")
        self._initialize(parent=parent, obj=axis, grid_type=grid_type)

    def _html_args(self):
        return {'grid_type': json.dumps(self.grid_type)}

    def _style_args(self):
        gridlines = getattr(self.ax, self.grid_type + 'axis').get_gridlines()
        color = color_to_hex(gridlines[0].get_color())
        alpha = gridlines[0].get_alpha()
        dasharray = get_dasharray(gridlines[0])
        return dict(color=color,
                    dasharray=dasharray,
                    alpha=alpha)


class D3Text(D3Base):
    """Class for representing matplotlib text in D3js"""

    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    text.text{{ elid }} {
       font-size : {{ fontsize }}px;
       fill : {{ color }};
       opacity : {{ alpha }};
    }
    """)

    HTML = jinja2.Template("""
    {% if text != '""' %}
    // Add a text element
    {{ axvar }}.add_element(new function(){
     this.position = {{ position }};
     this.rotation = {{ rotation }};
     this.ax = {{ axvar }};
     this.text = {{ text }};

     this.draw = function(){
       {% if zoomable %}
       this.obj = this.ax.axes.append("text")
                         .attr("x", this.ax.x(this.position[0]))
                         .attr("y", this.ax.y(this.position[1]))
                         {% if rotation %}
                         .attr("transform", "rotate(" + this.rotation + ","
                                          + this.ax.x(this.position[0]) + ","
                                          + this.ax.y(this.position[1]) + ")")
                         {% endif %}
       {% else %}
       this.obj = this.ax.fig.canvas.append("text")
                      .attr("x", this.position[0])
                      .attr("y", this.ax.fig.height - this.position[1])
                      {% if rotation %}
                      .attr("transform", "rotate(" + this.rotation + ","
                                      + this.position[0] + ","
                                      + (figheight - this.position[1]) + ")")
                      {% endif %}
       {% endif %}
                      .attr("class", "text")
                      .text(this.text)
                      .attr("class", "text{{ elid }}")
                      .attr("style", "text-anchor: {{ h_anchor }};" +
                                     "dominant-baseline: {{ v_baseline }}")

     }

     this.zoomed = function(){
     {% if zoomable %}
     this.obj.attr("x", this.ax.x(this.position[0]))
             .attr("y", this.ax.y(this.position[1]))
             {% if rotation %}
             .attr("transform", "rotate(" + this.rotation + ","
                             + this.ax.x(this.position[0]) + ","
                             + this.ax.y(this.position[1]) + ")")
             {% endif %}
     {% endif %}
     }
    });
    {% endif %}
    """)

    def __init__(self, parent, text):
        self._initialize(parent=parent, obj=text, text=text)

    def zoomable(self):
        return self.text.get_transform().contains_branch(self.ax.transData)

    def get_position(self):
        if self.zoomable():
            transform = self.text.get_transform() - self.ax.transData
        else:
            transform = self.text.get_transform()

        x, y = transform.transform(self.text.get_position())

        return x, y

    def get_rotation(self):
        return -self.text.get_rotation()

    def _style_args(self):
        alpha = self.text.get_alpha()
        if alpha is None:
            alpha = 1
        color = color_to_hex(self.text.get_color())
        fontsize = self.text.get_size()

        return dict(color=color,
                    fontsize=fontsize,
                    alpha=alpha)

    def _html_args(self):
        va_dict = {'bottom': 'auto',
                   'baseline': 'auto',
                   'center': 'central',
                   'top': 'hanging'}
        ha_dict = {'left': 'start',
                   'center': 'middle',
                   'right': 'end'}

        v_baseline = va_dict[self.text.get_verticalalignment()]
        h_anchor = ha_dict[self.text.get_horizontalalignment()]

        return dict(zoomable=self.zoomable(),
                    position=json.dumps(self.get_position()),
                    text=json.dumps(self.text.get_text()),
                    rotation=json.dumps(self.get_rotation()),
                    h_anchor=h_anchor,
                    v_baseline=v_baseline)


class D3Line2D(D3Base):
    """Class for representing a 2D matplotlib line in D3js"""

    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    .axes{{ axid }}
    path.line{{ lineid }} {
        stroke: {{ linecolor }};
        stroke-width: {{ linewidth }};
        stroke-dasharray: {{ dasharray }};
        fill: none;
        stroke-opacity: {{ alpha }};
    }

    div#figure{{ figid }}
    .axes{{ axid }}
    path.points{{ lineid }} {
        stroke-width: {{ markeredgewidth }};
        stroke: {{ markeredgecolor }};
        fill: {{ markercolor }};
        fill-opacity: {{ alpha }};
        stroke-opacity: {{ alpha }};
    }
    """)

    HTML = jinja2.Template("""
    // Add a Line2D element
    var line{{ elid }} = new function(){
     this.data = {{ data }};
     this.ax = {{ axvar }};

     this.translate = function(d)
       { return "translate(" + this.ax.x(d[0]) + ","
                             + this.ax.y(d[1]) + ")"; };

     this.draw = function(){
       {% if obj.has_line() %}
         this.line = d3.svg.line()
              .x(function(d) {return this.ax.x(d[0]);})
              .y(function(d) {return this.ax.y(d[1]);})
              .interpolate("linear")
              .defined(function (d) {return !isNaN(d[0]) && !isNaN(d[1]); });

         this.lineobj = this.ax.axes.append("svg:path")
                             .attr("d", this.line(this.data))
                             .attr('class', 'line{{ lineid }}');
       {% endif %}
       {% if obj.has_points() %}
         this.pointsobj = this.ax.axes.append("svg:g")
             .selectAll("scatter-dots-{{ lineid }}")
               .data(this.data.filter(
                           function(d){return !isNaN(d[0]) && !isNaN(d[1]); }))
               .enter().append("svg:path")
                   .attr('class', 'points{{ lineid }}')
                   .attr("d", construct_SVG_path({{ markerpath }}))
                   .attr("transform", this.translate.bind(this));
       {% endif %}
     };

     this.zoomed = function(){
        {% if obj.zoomable() %}
          {% if obj.has_line() %}
            this.lineobj.attr("d", this.line(this.data));
          {% endif %}
          {% if obj.has_points() %}
            this.pointsobj.attr("transform", this.translate.bind(this));
          {% endif %}
        {% endif %}
     }
    };

    {{ axvar }}.add_element(line{{ elid }});
    """)

    def __init__(self, parent, line):
        self._initialize(parent=parent, obj=line, line=line)
        self.lineid = self.elcount

    def zoomable(self):
        return self.line.get_transform().contains_branch(self.ax.transData)

    def has_line(self):
        return self.line.get_linestyle() not in ['', ' ', 'None', 'none', None]

    def has_points(self):
        return self.line.get_marker() not in ['', ' ', 'None', 'none', None]

    def _style_args(self):
        alpha = self.line.get_alpha()
        if alpha is None:
            alpha = 1
        lc = color_to_hex(self.line.get_color())
        lw = self.line.get_linewidth()
        mc = color_to_hex(self.line.get_markerfacecolor())
        mec = color_to_hex(self.line.get_markeredgecolor())
        mew = self.line.get_markeredgewidth()
        dasharray = get_dasharray(self.line)

        return dict(lineid=self.lineid,
                    linecolor=lc,
                    linewidth=lw,
                    markeredgewidth=mew,
                    markeredgecolor=mec,
                    markercolor=mc,
                    dasharray=dasharray,
                    alpha=alpha)

    def _html_args(self):
        transform = self.line.get_transform() - self.ax.transData
        data = transform.transform(self.line.get_xydata()).tolist()

        markerstyle = MarkerStyle(self.line.get_marker())
        markersize = self.line.get_markersize()
        markerpath = path_data(markerstyle.get_path(),
                               (markerstyle.get_transform()
                                + Affine2D().scale(markersize, -markersize)))

        return dict(lineid=self.lineid,
                    data=json.dumps(data),
                    markerpath=json.dumps(markerpath),
                    markersize=markersize)


class D3Patch(D3Base):
    """Class for representing matplotlib patches in D3js"""
    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    .axes{{ axid }}
    path.patch{{ patchid }} {
        stroke: {{ linecolor }};
        stroke-width: {{ linewidth }};
        stroke-dasharray: {{ dasharray }};
        fill: {{ fillcolor }};
        stroke-opacity: {{ alpha }};
        fill-opacity: {{ alpha }};
    }
    """)

    HTML = jinja2.Template("""
    // Add a Patch element
    var patch{{ elid }} = new function(){
      this.data = {{ data }};
      this.ax = {{ axvar }};

      this.draw = function(){
        this.patch = this.ax.axes.append("svg:path")
                       .attr("d", construct_SVG_path(this.data,
                                                     this.ax.x,
                                                     this.ax.y))
                       .attr("vector-effect", "non-scaling-stroke")
                       .attr('class', 'patch{{ patchid }}');
      };

      this.zoomed = function(){
        {% if obj.zoomable() %}
          this.patch.attr("d", construct_SVG_path(this.data,
                                                  this.ax.x,
                                                  this.ax.y));
        {% endif %}
      };
    };

    {{ axvar }}.add_element(patch{{ elid }});
    """)

    def __init__(self, parent, patch):
        self._initialize(parent=parent, obj=patch, patch=patch)
        self.patchid = self.elid

    def zoomable(self):
        return self.patch.get_transform().contains_branch(self.ax.transData)

    def _style_args(self):
        ec = self.patch.get_edgecolor()
        if self.patch.get_fill():
            fc = color_to_hex(self.patch.get_facecolor())
        else:
            fc = "none"

        alpha = self.patch.get_alpha()
        if alpha is None:
            alpha = 1
        lc = color_to_hex(self.patch.get_edgecolor())
        lw = self.patch.get_linewidth()
        dasharray = get_dasharray(self.patch)

        return dict(patchid=self.patchid,
                    linecolor=lc,
                    linewidth=lw,
                    fillcolor=fc,
                    dasharray=dasharray,
                    alpha=alpha)

    def _html_args(self):
        # transform path to data coordinates
        transform = self.patch.get_transform() - self.ax.transData
        data = path_data(self.patch.get_path(), transform)
        return dict(patchid=self.patchid,
                    data=json.dumps(data))


class D3Image(D3Base):
    """Class for representing matplotlib images in D3js"""
    # TODO: - Can rendering be done in-browser?

    STYLE = jinja2.Template("""
    div#figure{{ figid }}
    .axes{{ axid }}
    image.image{{ imageid }} {
       opacity: {{ alpha }};
    }
    """)

    HTML = jinja2.Template("""
    // Add an Image element
    var image{{ elid }} = new function(){
      this.ax = {{ axvar }};
      this.data = "data:image/png;base64," + "{{ base64_data }}";
      this.extent = {{ extent }};
      this.class = "image{{ imageid }}";

      this.draw = function(){
        this.image = this.ax.axes.append("svg:image")
            .attr('class', this.class)
            .attr("xlink:href", this.data)
            .attr("preserveAspectRatio", "none");
        this.zoomed();  // set the initial image location
      };

      this.zoomed = function(){
        this.image.attr("x", this.ax.x(this.extent[0]))
                  .attr("y", this.ax.y(this.extent[3]))
                  .attr("width", this.ax.x(this.extent[1])
                                  - this.ax.x(this.extent[0]))
                  .attr("height", this.ax.y(this.extent[2])
                                  - this.ax.y(this.extent[3]));
      };
    };
    {{ axvar }}.add_element(image{{ elid }});
    """)

    def __init__(self, parent, image):
        self._initialize(parent=parent, obj=image, image=image)
        self.imageid = self.elid

    def get_base64_data(self):
        binary_buffer = io.BytesIO()

        # image is saved in axes coordinates: we need to temporarily
        # set the correct limits to get the correct image, then undo it.
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(self.image.get_extent()[:2])
        self.ax.set_ylim(self.image.get_extent()[2:])
        self.image.write_png(binary_buffer)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        binary_buffer.seek(0)
        return base64.b64encode(binary_buffer.read()).decode('utf-8')

    def _html_args(self):
        return dict(imageid=self.imageid,
                    base64_data=self.get_base64_data(),
                    extent=json.dumps(self.image.get_extent()))

    def _style_args(self):
        return dict(imageid=self.imageid,
                    alpha=self.image.get_alpha())


class D3Collection(D3Base):
    """Class for representing matplotlib path collections in D3js"""

    # TODO: when all paths have same offset, or all offsets have same paths,
    #       this can be done more efficiently.  Also, defaults should be
    #       done at the template level rather than the javascript level.

    HTML = jinja2.Template("""
    // Add a Collection
    var coll{{ elid }} = new function(){
      this.ax = {{ axvar }};
      this.data = {{ data }};

      this.offset_func = function(d){
         var offset = d.o ? d.o : {{ defaults.o }};
         {% if obj.offset_zoomable() %}
           offset = [this.ax.x(offset[0]), this.ax.y(offset[1])];
         {% endif %}
         return "translate(" + offset  + ")";
      };

      this.path_func = function(d){
         var path = d.p ? d.p : {{ defaults.p }};
         var size = d.s ? d.s : {{ defaults.s }};
         {% if obj.path_zoomable() %}
           var xscale = function(x){return this.ax.x(size * x);}.bind(this);
           var yscale = function(y){return this.ax.y(size * y);}.bind(this);
         {% else %}
           var xscale = function(x){return size * x;};
           var yscale = function(y){return size * y;};
         {% endif %}
         return construct_SVG_path(path, xscale, yscale);
      };

      this.style_func = function(d){
         var edgecolor = d.ec ? d.ec : {{ defaults.ec }};
         var facecolor = d.fc ? d.fc : {{ defaults.fc }};
         var linewidth = d.lw ? d.lw : {{ defaults.lw }};
         var dasharray = d.ls ? d.ls : {{ defaults.ls }};
         return "stroke: " + edgecolor + "; " +
                "stroke-width: " + linewidth + "; " +
                "stroke-dasharray: " + dasharray + "; " +
                "fill: " + facecolor + "; " +
                "stroke-opacity: {{ defaults.alpha }}; " +
                "fill-opacity: {{ defaults.alpha }}";
      };

      this.draw = function(){
        this.g = this.ax.axes.append("svg:g");

        this.g.selectAll("paths-{{ collid }}")
          .data(this.data)
          .enter().append("svg:path")
              .attr('class', 'paths{{ collid }}')
              .attr("d", this.path_func.bind(this))
              .attr("style", this.style_func.bind(this))
              .attr("transform", this.offset_func.bind(this));
      };

      this.zoomed = function(){
        this.g.selectAll(".paths{{ collid }}")
                 {% if obj.path_zoomable() %}
                   .attr("d", this.path_func.bind(this))
                 {% endif %}
                 {% if obj.offset_zoomable() %}
                   .attr("transform", this.offset_func.bind(this))
                 {% endif %};
      };
    };
    {{ axvar }}.add_element(coll{{ elid }});
    """)

    def __init__(self, parent, collection):
        self._initialize(parent, obj=collection, collection=collection)
        self.collid = self.elcount

    def _update_data(self, data, defaults):
        return data, defaults

    def offset_zoomable(self):
        transform = self.collection.get_offset_transform()
        return transform.contains_branch(self.ax.transData)

    def get_offset_transform(self):
        if self.offset_zoomable():
            return self.collection.get_offset_transform() - self.ax.transData
        else:
            return self.collection.get_offset_transform()

    def path_zoomable(self):
        transform = self.collection.get_transform()
        return transform.contains_branch(self.ax.transData)

    def get_path_transform(self):
        if self.path_zoomable():
            return self.collection.get_transform() - self.ax.transData
        else:
            # pixel coordinates start at top; we need to flip the path here
            return self.collection.get_transform() + Affine2D().scale(1., -1.)

    def get_data_defaults(self):
        offset_transform = self.get_offset_transform()
        path_transform = self.get_path_transform()

        offsets = [offset_transform.transform(offset).tolist()
                   for offset in self.collection.get_offsets()]
        paths = [path_data(path, path_transform)
                 for path in self.collection.get_paths()]

        data = {'o': offsets,
                'p': paths}
        defaults = {'o': [[0, 0]]}

        self.collection.update_scalarmappable()  # this updates colors
        data['ec'] = list(map(color_to_hex, self.collection.get_edgecolors()))
        defaults['ec'] = 'none'

        data['fc'] = list(map(color_to_hex, self.collection.get_facecolors()))
        defaults['fc'] = 'none'

        data['alpha'] = self.collection.get_alpha()
        defaults['alpha'] = 1

        data['lw'] = self.collection.get_linewidths()
        defaults['lw'] = 1

        data['ls'] = [get_dasharray(self.collection, i)
                      for i in range(len(self.collection.get_linestyles()))]
        defaults['ls'] = "10,0"

        # make the size scaling default equal to 1
        data['s'] = 1

        # process the data and defaults
        data, defaults = self._update_data(data, defaults)
        data, defaults = collection_data(data, defaults)

        return data, defaults

    def _html_args(self):
        if self.collection.get_transforms() != []:
            warnings.warn("Collection: multiple transforms not implemented. "
                          "They will be ignored.")

        data, defaults = self.get_data_defaults()

        return dict(collid=self.collid,
                    data=json.dumps(data),
                    defaults=defaults)


class D3PathCollection(D3Collection):
    def _update_data(self, data, defaults):
        defaults['s'] = 1
        sizes = self.collection.get_sizes()
        if sizes is not None:
            sizes = np.sqrt(sizes) * self.fig.dpi / 72.
        data['s'] = sizes
        return data, defaults


class D3QuadMesh(D3Collection):
    def __init__(self, *args, **kwargs):
        warnings.warn("Not all QuadMesh features are yet implemented")
        D3Collection.__init__(self, *args, **kwargs)


class D3LineCollection(D3Collection):
    def _update_data(self, data, defaults):
        # Hack to make length of paths match length of colors.
        # not sure why there is one more color than the number of paths.
        data['p'].append([['M', [0, 0]]])

        return data, defaults


class D3PatchCollection(D3Collection):
    """Class for representing matplotlib patch collections in D3js"""
    # TODO: there are special D3 classes for many common patch types
    #       (i.e. circle, ellipse, rectangle, polygon, etc.)  We should
    #       use these where possible.
    pass
