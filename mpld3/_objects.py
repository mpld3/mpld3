import abc
import uuid
import warnings
from collections import defaultdict
import base64
import io

from ._utils import get_figtext_coordinates, color_to_hex, \
    get_dasharray, get_d3_shape_for_marker

import matplotlib


class D3Base(object):
    """Abstract Base Class for D3js objects"""
    __metaclass__ = abc.ABCMeta

    # keep track of the number of children of each element:
    # this assists in generating unique ids for all HTML elements
    num_children_by_id = defaultdict(int)

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4()).replace('-', '')

    def _initialize(self, parent=None, **kwds):
        # set attributes
        self.parent = parent
        for key, val in kwds.items():
            setattr(self, key, val)

        # create a unique element id
        if parent is None:
            self.elid = self.generate_unique_id()
        else:
            self.num_children_by_id[self.parent.elid] += 1
            self.elid = (self.parent.elid +
                         str(self.num_children_by_id[self.parent.elid]))

    def __getattr__(self, attr):
        if attr in ['fig', 'ax', 'figid', 'axid']:
            if hasattr(self, '_' + attr):
                return getattr(self, '_' + attr)
            elif self.parent is not None and self.parent is not self:
                return getattr(self.parent, attr)
        else:
            raise AttributeError("no attribute {0}".format(attr))

    @abc.abstractmethod
    def html(self):
        raise NotImplementedError()

    def style(self):
        return ''

    def zoom(self):
        return ''

    def __str__(self):
        return self.html()


class D3Figure(D3Base):
    """Class for representing a matplotlib Figure in D3js"""
    D3_WEB_LOC = "http://d3js.org/d3.v3.min.js"

    D3_IMPORT = """
    <script type="text/javascript" src="{d3_url}"></script>
    """

    STYLE = """
    <style>
    {styles}
    </style>
    """

    FIGURE_TEMPLATE = """
    <div id='figure{figid}'></div>

    <script type="text/javascript">
    func{figid} = function(figure){{

    var figwidth = {figwidth} * {dpi};
    var figheight = {figheight} * {dpi};

    var canvas = figure.append('svg:svg')
                   .attr('width', figwidth)
                   .attr('height', figheight)
                   .attr('class', 'canvas')

    {axes}

    }}

    // set a timeout of 0 to allow d3.js to load
    setTimeout(function(){{ func{figid}(d3.select('#figure{figid}')) }}, 0)
    </script>
    """

    def __init__(self, fig):
        # use time() to make sure multiple versions of this figure
        # don't cross-talk if used on the same page.
        self._initialize(parent=None, _fig=fig, _ax=None)
        self._figid = self.elid
        self.axes = [D3Axes(self, ax) for ax in fig.axes]

    def d3_import(self, d3_url=None):
        if d3_url is None:
            d3_url = self.D3_WEB_LOC
        return self.D3_IMPORT.format(d3_url=d3_url)

    def style(self):
        return self.STYLE.format(styles='\n'.join([ax.style()
                                                   for ax in self.axes]))

    def html(self, d3_url=None, with_d3_import=True, with_style=True):
        result = ""
        if with_d3_import:
            result += self.d3_import(d3_url)
        if with_style:
            result += self.style()

        axes = '\n'.join(ax.html() for ax in self.axes)
        fig = self.FIGURE_TEMPLATE.format(figid=self.figid,
                                          figwidth=self.fig.get_figwidth(),
                                          figheight=self.fig.get_figheight(),
                                          dpi=self.fig.dpi,
                                          axes=axes)
        return result + fig


class D3Axes(D3Base):
    """Class for representing a matplotlib Axes in D3js"""
    STYLE = """
    div#figure{figid}
    .axes{axid}.axis line, .axes{axid}.axis path {{
        shape-rendering: crispEdges;
        stroke: black;
        fill: none;
    }}

    div#figure{figid}
    .axes{axid}.axis text {{
        font-family: sans-serif;
        font-size: {fontsize}px;
        fill: black;
        stroke: none;
    }}
    """

    XAXIS_TEMPLATE = """
    var x_{axid} = d3.scale.linear()
                     .domain([{xlim[0]}, {xlim[1]}])
                     .range([0, width_{axid}]);
    var x_data_map{axid} = x_{axid};
    """

    LOG_XAXIS_TEMPLATE = """
    var x_{axid} = d3.scale.log()
                     .domain([{xlim[0]}, {xlim[1]}])
                     .range([0, width_{axid}]);
    var x_data_map{axid} = x_{axid};
    """

    DATE_XAXIS_TEMPLATE = """
    var start_date_x{axid} = new Date({d0[0]}, {d0[1]}, {d0[2]}, {d0[3]},
                                      {d0[4]}, {d0[5]}, {d0[6]});
    var end_date_x{axid} = new Date({d1[0]}, {d1[1]}, {d1[2]}, {d1[3]},
                                    {d1[4]}, {d1[5]}, {d1[6]});

    var x_{axid} = d3.time.scale()
                      .domain([start_date_x{axid}, end_date_x{axid}])
                      .range([0, width_{axid}]);

    var x_reverse_date_scale_{axid} = d3.time.scale()
                                        .domain([start_date_x{axid},
                                                 end_date_x{axid}])
                                        .range([{xlim[0]}, {xlim[1]}]);

    var x_data_map{axid} = function (x)
                {{ return x_{axid}(x_reverse_date_scale_{axid}.invert(x));}}
    """

    YAXIS_TEMPLATE = """
    var y_{axid} = d3.scale.linear()
                           .domain([{ylim[0]}, {ylim[1]}])
                           .range([height_{axid}, 0]);
    var y_data_map{axid} = y_{axid};
    """

    LOG_YAXIS_TEMPLATE = """
    var y_{axid} = d3.scale.log()
                           .domain([{ylim[0]}, {ylim[1]}])
                           .range([height_{axid}, 0]);
    var y_data_map{axid} = y_{axid};
    """

    DATE_YAXIS_TEMPLATE = """
    var start_date_y{axid} = new Date({d0[0]}, {d0[1]}, {d0[2]}, {d0[3]},
                                      {d0[4]}, {d0[5]}, {d0[6]});
    var end_date_y{axid} = new Date({d1[0]}, {d1[1]}, {d1[2]}, {d1[3]},
                                    {d1[4]}, {d1[5]}, {d1[6]});

    var y_{axid} = d3.time.scale()
                      .domain([end_date_y{axid}, start_date_y{axid}])
                      .range([0, width_{axid}]);

    var y_reverse_date_scale_{axid} = d3.time.scale()
                                             .domain([start_date_y{axid},
                                                      end_date_y{axid}])
                                             .range([{ylim[0]}, {ylim[1]}]);

    var y_data_map{axid} = function (y)
                {{ return y_{axid}(y_reverse_date_scale_{axid}.invert(y));}}
    """

    AXES_TEMPLATE = """
    // store the width and height of the axes
    var width_{axid} = {bbox[2]} * figwidth;
    var height_{axid} = {bbox[3]} * figheight

    {xaxis_code}
    {yaxis_code}


    // zoom object for the axes
    var zoom{axid} = d3.behavior.zoom()
                    .x(x_{axid})
                    .y(y_{axid})
                    .on("zoom", zoomed{axid});

    // create the axes itself
    var baseaxes_{axid} = canvas.append('g')
            .attr('transform', 'translate(' + ({bbox[0]} * figwidth) + ',' +
                              ((1 - {bbox[1]} - {bbox[3]}) * figheight) + ')')
            .attr('width', width_{axid})
            .attr('height', height_{axid})
            .attr('class', 'main')
            .call(zoom{axid});

    // create the axes background
    baseaxes_{axid}.append("svg:rect")
                      .attr("width", width_{axid})
                      .attr("height", height_{axid})
                      .attr("class", "bg{axid}")
                      .attr("fill", "{axesbg}");

    // axis factory functions: used for grid lines & axes
    var create_xAxis_{axid} = function(){{
       return d3.svg.axis()
            .scale(x_{axid})
            .orient('bottom');
    }}

    var create_yAxis_{axid} = function(){{
       return d3.svg.axis()
            .scale(y_{axid})
            .orient('left');
    }}

    // draw the x axis
    var xAxis_{axid} = create_xAxis_{axid}();

    baseaxes_{axid}.append('g')
            .attr('transform', 'translate(0,' + (height_{axid}) + ')')
            .attr('class', 'axes{axid} x axis')
            .call(xAxis_{axid});

    // draw the y axis
    var yAxis_{axid} = create_yAxis_{axid}();

    baseaxes_{axid}.append('g')
            .attr('transform', 'translate(0,0)')
            .attr('class', 'axes{axid} y axis')
            .call(yAxis_{axid});

    // create the clip boundary
    var clip_{axid} = baseaxes_{axid}.append("svg:clipPath")
                             .attr("id", "clip{axid}")
                             .append("svg:rect")
                             .attr("x", 0)
                             .attr("y", 0)
                             .attr("width", width_{axid})
                             .attr("height", height_{axid});

    // axes_{axid} is the axes on which to draw plot components: they'll
    // be clipped when zooming or scrolling moves them out of the plot.
    var axes_{axid} = baseaxes_{axid}.append('g')
            .attr("clip-path", "url(#clip{axid})");

    {elements}

    function zoomed{axid}() {{
        //console.log(d3.event.translate);
        //console.log(d3.event.scale);
        baseaxes_{axid}.select(".x.axis").call(xAxis_{axid});
        baseaxes_{axid}.select(".y.axis").call(yAxis_{axid});

        {element_zooms}
    }}
    """

    def __init__(self, parent, ax):
        # import here in case people call matplotlib.use()
        import matplotlib as mpl

        self._initialize(parent=parent, _ax=ax)
        self._axid = self.elid
        self.lines = [D3Line2D(self, line) for line in ax.lines]
        self.texts = [D3Text(self, text) for text in ax.texts]
        self.texts += [D3Text(self, text) for text in [ax.xaxis.label,
                                                       ax.yaxis.label,
                                                       ax.title]]
        self.images = [D3Image(self, ax, image) for image in ax.images]
        self.grids = [D3Grid(self)]
        self.patches = [D3Patch(self, patch)
                        for i, patch in enumerate(ax.patches)]
        self.collections = []

        for collection in ax.collections:
            if isinstance(collection, mpl.collections.PolyCollection):
                self.collections.append(D3PatchCollection(self, collection))
            else:
                warnings.warn("{0} not implemented.  "
                              "Elements will be ignored".format(collection))

        # Some warnings for pieces of matplotlib which are not yet implemented
        for attr in ['artists', 'tables']:
            if len(getattr(ax, attr)) > 0:
                warnings.warn("{0} not implemented.  "
                              "Elements will be ignored".format(attr))

        if ax.legend_ is not None:
            warnings.warn("legend is not implemented: it will be ignored")

    def style(self):
        ticks = self.ax.xaxis.get_ticklabels() + self.ax.yaxis.get_ticklabels()
        if len(ticks) == 0:
            fontsize_x = 11
        else:
            fontsize_x = ticks[0].properties()['size']
        return '\n'.join([self.STYLE.format(axid=self.axid,
                                            figid=self.figid,
                                            fontsize=fontsize_x)] +
                         [g.style() for g in self.grids] +
                         [l.style() for l in self.lines] +
                         [t.style() for t in self.texts] +
                         [p.style() for p in self.patches] +
                         [c.style() for c in self.collections])

    def html(self):
        elements = '\n'.join([elem.html() for elem in
                              (self.images + self.grids + self.patches +
                               self.lines + self.texts + self.collections)])
        zooms = '\n'.join(elem.zoom() for elem in
                          (self.images + self.grids + self.patches +
                           self.lines + self.texts + self.collections))

        axisbg = color_to_hex(self.ax.patch.get_facecolor())

        if isinstance(self.ax.xaxis.converter, matplotlib.dates.DateConverter):
            date0, date1 = matplotlib.dates.num2date(self.ax.get_xlim())
            d0 = [date0.year, date0.month - 1, date0.day, date0.hour,
                  date0.minute, date0.second, date0.microsecond / 1e3]
            d1 = [date1.year, date1.month - 1, date1.day, date1.hour,
                  date1.minute, date1.second, date1.microsecond / 1e3]
            template = self.DATE_XAXIS_TEMPLATE
            xaxis_code = template.format(axid=self.axid,
                                         xlim=self.ax.get_xlim(),
                                         d0=d0, d1=d1)
        else:
            if self.ax.get_xscale() == 'log':
                template = self.LOG_XAXIS_TEMPLATE
            elif self.ax.get_xscale() == 'linear':
                template = self.XAXIS_TEMPLATE
            else:
                assert False, "unknown axis scale"
            xaxis_code = template.format(axid=self.axid,
                                         xlim=self.ax.get_xlim())

        if isinstance(self.ax.yaxis.converter, matplotlib.dates.DateConverter):
            date0, date1 = matplotlib.dates.num2date(self.ax.get_ylim())
            d0 = [date0.year, date0.month - 1, date0.day, date0.hour,
                  date0.minute, date0.second, date0.microsecond / 1e3]
            d1 = [date1.year, date1.month - 1, date1.day, date1.hour,
                  date1.minute, date1.second, date1.microsecond / 1e3]
            template = self.DATE_YAXIS_TEMPLATE
            yaxis_code = template.format(axid=self.axid,
                                         ylim=self.ax.get_ylim(),
                                         d0=d0, d1=d1)
        else:
            if self.ax.get_yscale() == 'log':
                template = self.LOG_YAXIS_TEMPLATE
            elif self.ax.get_yscale() == 'linear':
                template = self.YAXIS_TEMPLATE
            else:
                assert False, "unknown axis scale"
            yaxis_code = template.format(axid=self.axid,
                                         ylim=self.ax.get_ylim())

        return self.AXES_TEMPLATE.format(id=id(self.ax),
                                         axid=self.axid,
                                         xaxis_code=xaxis_code,
                                         yaxis_code=yaxis_code,
                                         bbox=self.ax.get_position().bounds,
                                         axesbg=axisbg,
                                         elements=elements,
                                         element_zooms=zooms)


class D3Grid(D3Base):
    """Class for representing a matplotlib Axes grid in D3js"""
    STYLE = """
    div#figure{figid}
    .grid .tick {{
      stroke: {color};
      stroke-dasharray: {dasharray};
      stroke-opacity: {alpha};
    }}

    div#figure{figid}
    .grid path {{
      stroke-width: 0;
    }}
    """

    XGRID_TEMPLATE = """
    // draw x grid lines: we use a second x-axis with long ticks
    axes_{axid}.append("g")
         .attr("class", "axes{axid} x grid")
         .attr("transform", "translate(0," + (height_{axid}) + ")")
         .call(create_xAxis_{axid}()
                       .tickSize(-(height_{axid}), 0, 0)
                       .tickFormat(""));
    """

    YGRID_TEMPLATE = """
    // draw y grid lines: we use a second y-axis with long ticks
    axes_{axid}.append("g")
         .attr("class", "axes{axid} y grid")
         .call(create_yAxis_{axid}()
                       .tickSize(-(width_{axid}), 0, 0)
                       .tickFormat(""));
    """

    XZOOM = """
        axes_{axid}.select(".x.grid")
            .call(create_xAxis_{axid}()
            .tickSize(-(height_{axid}), 0, 0)
            .tickFormat(""));
    """

    YZOOM = """
        axes_{axid}.select(".y.grid")
            .call(create_yAxis_{axid}()
            .tickSize(-(width_{axid}), 0, 0)
            .tickFormat(""));
    """

    def __init__(self, parent):
        self._initialize(parent=parent)

    def zoom(self):
        ret = ""
        bbox = self.ax.get_position().bounds
        if self.ax.xaxis._gridOnMajor:
            ret += self.XZOOM.format(axid=self.axid,
                                     bbox=bbox)
        if self.ax.yaxis._gridOnMajor:
            ret += self.YZOOM.format(axid=self.axid,
                                     bbox=bbox)
        return ret

    def html(self):
        ret = ""
        bbox = self.ax.get_position().bounds
        if self.ax.xaxis._gridOnMajor:
            ret += self.XGRID_TEMPLATE.format(axid=self.axid,
                                              bbox=bbox)
        if self.ax.yaxis._gridOnMajor:
            ret += self.YGRID_TEMPLATE.format(axid=self.axid,
                                              bbox=bbox)
        return ret

    def style(self):
        gridlines = (self.ax.xaxis.get_gridlines() +
                     self.ax.yaxis.get_gridlines())
        color = color_to_hex(gridlines[0].get_color())
        alpha = gridlines[0].get_alpha()
        dasharray = get_dasharray(gridlines[0])
        return self.STYLE.format(color=color,
                                 alpha=alpha,
                                 figid=self.figid,
                                 dasharray=dasharray)


class D3Line2D(D3Base):
    """Class for representing a 2D matplotlib line in D3js"""
    DATA_TEMPLATE = """
    var data_{lineid} = {data}
    """

    STYLE = """
    div#figure{figid}
    path.line{lineid} {{
        stroke: {linecolor};
        stroke-width: {linewidth};
        stroke-dasharray: {dasharray};
        fill: none;
        stroke-opacity: {alpha};
    }}

    div#figure{figid}
    path.points{lineid} {{
        stroke-width: {markeredgewidth};
        stroke: {markeredgecolor};
        fill: {markercolor};
        fill-opacity: {alpha};
        stroke-opacity: {alpha};
    }}
    """

    LINE_ZOOM = """
        axes_{axid}.select(".line{lineid}")
                       .attr("d", line_{lineid}(data_{lineid}));
    """

    POINTS_ZOOM = """
        axes_{axid}.selectAll(".points{lineid}")
              .attr("transform", function(d)
                {{ return "translate(" + x_data_map{axid}(d[0]) + "," +
                   y_data_map{axid}(d[1]) + ")"; }});
    """

    LINE_TEMPLATE = """
    var line_{lineid} = d3.svg.line()
         .x(function(d) {{return x_data_map{axid}(d[0]);}})
         .y(function(d) {{return y_data_map{axid}(d[1]);}})
         .interpolate("linear");

    axes_{axid}.append("svg:path")
                   .attr("d", line_{lineid}(data_{lineid}))
                   .attr('class', 'line{lineid}');
    """

    POINTS_TEMPLATE = """
    var g_{lineid} = axes_{axid}.append("svg:g");

    g_{lineid}.selectAll("scatter-dots-{lineid}")
          .data(data_{lineid})
          .enter().append("svg:path")
              .attr('class', 'points{lineid}')
              .attr("d", d3.svg.symbol()
                            .type("{markershape}")
                            .size({markersize}))
              .attr("transform", function(d)
                  {{ return "translate(" + x_data_map{axid}(d[0]) +
                     "," + y_data_map{axid}(d[1]) + ")"; }});
    """

    def __init__(self, parent, line):
        self._initialize(parent=parent, line=line)
        self.lineid = self.elid

    def has_line(self):
        return self.line.get_linestyle() not in ['', ' ', 'None',
                                                 'none', None]

    def has_points(self):
        return self.line.get_marker() not in ['', ' ', 'None', 'none', None]

    def zoom(self):
        ret = ""
        if self.has_points():
            ret += self.POINTS_ZOOM.format(lineid=self.lineid,
                                           axid=self.axid)
        if self.has_line():
            ret += self.LINE_ZOOM.format(lineid=self.lineid,
                                         axid=self.axid)
        return ret

    def style(self):
        alpha = self.line.get_alpha()
        if alpha is None:
            alpha = 1
        lc = color_to_hex(self.line.get_color())
        lw = self.line.get_linewidth()
        mc = color_to_hex(self.line.get_markerfacecolor())
        mec = color_to_hex(self.line.get_markeredgecolor())
        mew = self.line.get_markeredgewidth()
        dasharray = get_dasharray(self.line)

        return self.STYLE.format(figid=self.figid,
                                 lineid=self.lineid,
                                 linecolor=lc,
                                 linewidth=lw,
                                 markeredgewidth=mew,
                                 markeredgecolor=mec,
                                 markercolor=mc,
                                 dasharray=dasharray,
                                 alpha=alpha)

    def html(self):
        data = self.line.get_xydata().tolist()
        result = self.DATA_TEMPLATE.format(lineid=self.lineid, data=data)

        if self.has_points():
            marker = self.line.get_marker()
            msh = get_d3_shape_for_marker(marker)
            ms = self.line.get_markersize() ** 2
            result += self.POINTS_TEMPLATE.format(lineid=self.lineid,
                                                  axid=self.axid,
                                                  markersize=ms,
                                                  markershape=msh,
                                                  data=data)
        if self.has_line():
            # TODO: use actual line style
            style = self.line.get_linestyle()
            result += self.LINE_TEMPLATE.format(lineid=self.lineid,
                                                axid=self.axid,
                                                data=data)
        return result


class D3Text(D3Base):
    """Class for representing matplotlib text in D3js"""
    FIG_TEXT_TEMPLATE = """
    canvas.append("text")
        .text("{text}")
        .attr("class", "text{textid}")
        .attr("x", {x})
        .attr("y", figheight - {y})
        .attr("font-size", "{fontsize}px")
        .attr("fill", "{color}")
        .attr("transform", "rotate({rotation},{x}," + (figheight - {y}) + ")")
        .attr("style", "text-anchor: {h_anchor};")
    """

    AXES_TEXT_TEMPLATE = """
    axes_{axid}.append("text")
        .text("{text}")
        .attr("class", "text{textid}")
        .attr("x", x_data_map{axid}({x}))
        .attr("y", y_data_map{axid}({y}))
        .attr("font-size", "{fontsize}px")
        .attr("fill", "{color}")
        .attr("transform", "rotate({rotation},{x}," + (figheight - {y}) + ")")
        .attr("style", "text-anchor: {h_anchor};")
    """

    AXES_TEXT_ZOOM = """
        axes_{axid}.select(".text{textid}")
                       .attr("x", x_data_map{axid}({x}))
                       .attr("y", y_data_map{axid}({y}))
    """

    def __init__(self, parent, text):
        self._initialize(parent=parent, text=text)
        self.textid = self.elid

    def is_axes_text(self):
        return (self.text.get_transform() is self.ax.transData)

    def zoom(self):
        if self.is_axes_text():
            x, y = self.text.get_position()
            return self.AXES_TEXT_ZOOM.format(axid=self.axid,
                                              textid=self.textid,
                                              x=x, y=y)
        else:
            return ''

    def html(self):
        text_content = self.text.get_text()

        if not text_content:
            return ''

        if self.is_axes_text():
            x, y = self.text.get_position()
            template = self.AXES_TEXT_TEMPLATE

        else:
            x, y = get_figtext_coordinates(self.text)
            template = self.FIG_TEXT_TEMPLATE

        color = color_to_hex(self.text.get_color())
        fontsize = self.text.get_size()
        rotation = -self.text.get_rotation()

        # TODO: fix vertical anchor point
        h_anchor = {'left': 'start',
                    'center': 'middle',
                    'right': 'end'}[self.text.get_horizontalalignment()]

        # hack for y-label alignment
        if self.text is self.ax.yaxis.label:
            x += fontsize

        return template.format(axid=self.axid,
                               textid=self.textid,
                               text=text_content,
                               x=x, y=y,
                               fontsize=fontsize,
                               color=color,
                               rotation=rotation,
                               h_anchor=h_anchor)


class D3Patch(D3Base):
    """Class for representing matplotlib patches in D3js"""
    STYLE = """
    div#figure{figid}
    path.patch{elid} {{
        stroke: {linecolor};
        stroke-width: {linewidth};
        stroke-dasharray: {dasharray};
        fill: {fillcolor};
        stroke-opacity: {alpha};
        fill-opacity: {alpha};
    }}
    """

    TEMPLATE = """
    var data_{elid} = {data}

    var patch_{elid} = d3.svg.line()
         .x(function(d) {{return x_data_map{axid}(d[0]);}})
         .y(function(d) {{return y_data_map{axid}(d[1]);}})
         .interpolate("{interpolate}");

    axes_{axid}.append("svg:path")
                   .attr("d", patch_{elid}(data_{elid}))
                   .attr('class', 'patch{elid}');
    """

    ZOOM = """
        axes_{axid}.select(".patch{elid}")
                       .attr("d", patch_{elid}(data_{elid}));
    """

    def __init__(self, parent, patch):
        self._initialize(parent=parent, patch=patch)
        self.patchid = self.elid

    def zoom(self):
        return self.ZOOM.format(axid=self.axid,
                                elid=self.elid)

    def style(self):
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

        return self.STYLE.format(figid=self.figid,
                                 elid=self.elid,
                                 linecolor=lc,
                                 linewidth=lw,
                                 fillcolor=fc,
                                 dasharray=dasharray,
                                 alpha=alpha)

    def html(self):
        path = self.patch.get_path()
        transform = self.patch.get_patch_transform()
        data = path.transformed(transform).vertices.tolist()
        # TODO: use appropriate interpolations
        interpolate = "linear"
        return self.TEMPLATE.format(axid=self.axid, elid=self.elid,
                                    data=data, interpolate=interpolate)


class D3PatchCollection(D3Base):
    """Class for representing matplotlib patche collections in D3js"""
    STYLE = """
    div#figure{figid}
    path.coll{elid}.patch{i} {{
        stroke: {linecolor};
        stroke-width: {linewidth};
        stroke-dasharray: {dasharray};
        fill: {fillcolor};
        stroke-opacity: {alpha};
        fill-opacity: {alpha};
    }}
    """

    TEMPLATE = """
    var data_{pathid} = {data}

    var patch_{pathid} = d3.svg.line()
         .x(function(d) {{return x_data_map{axid}(d[0]);}})
         .y(function(d) {{return y_data_map{axid}(d[1]);}})
         .interpolate("{interpolate}");

    axes_{axid}.append("svg:path")
                   .attr("d", patch_{pathid}(data_{pathid}))
                   .attr('class', 'coll{elid} patch{i}');
    """

    ZOOM = """
        axes_{axid}.select(".coll{elid}.patch{i}")
                       .attr("d", patch_{pathid}(data_{pathid}));
    """

    def __init__(self, parent, collection):
        self._initialize(parent=parent, collection=collection)
        self.n_paths = len(collection.get_paths())

    def pathid(self, i):
        return self.elid + str(i + 1)

    def zoom(self):
        return "".join([self.ZOOM.format(axid=self.axid,
                                         i=i + 1,
                                         pathid=self.pathid(i),
                                         elid=self.elid)
                        for i in range(self.n_paths)])

    def style(self):
        alpha = self.collection.get_alpha()
        if alpha is None:
            alpha = 1

        ec = self.collection.get_edgecolor()
        fc = self.collection.get_facecolor()
        lc = self.collection.get_edgecolor()
        lw = self.collection.get_linewidth()

        styles = []
        for i in range(self.n_paths):
            dasharray = get_dasharray(self.collection, i)
            styles.append(self.STYLE.format(figid=self.figid,
                                            elid=self.elid,
                                            i=i + 1,
                                            linecolor=color_to_hex(lc[i]),
                                            linewidth=lw[i],
                                            fillcolor=color_to_hex(fc[i]),
                                            dasharray=dasharray,
                                            alpha=alpha))
        return '\n'.join(styles)

    def html(self):
        results = []
        for i, path in enumerate(self.collection.get_paths()):
            data = path.vertices.tolist()
            # TODO: use appropriate interpolations
            interpolate = "linear"
            results.append(self.TEMPLATE.format(axid=self.axid,
                                                elid=self.elid,
                                                pathid=self.pathid(i),
                                                i=i + 1,
                                                data=data,
                                                interpolate=interpolate))
        return '\n'.join(results)


class D3Image(D3Base):
    """Class for representing matplotlib images in D3js"""
    IMAGE_TEMPLATE = """
    axes_{axid}.append("svg:image")
        .attr('class', 'image{imageid}')
        .attr("x", x_{axid}({x}))
        .attr("y", y_{axid}({y}))
        .attr("width", x_{axid}({width}) - x_{axid}({x}))
        .attr("height", y_{axid}({height}) - y_{axid}({y}))
        .attr("xlink:href", "data:image/png;base64," + "{base64_data}")
        .attr("preserveAspectRatio", "none");
    """

    IMAGE_ZOOM = """
        axes_{axid}.select(".image{imageid}")
                   .attr("x", x_{axid}({x}))
                   .attr("y", y_{axid}({y}))
                   .attr("width", x_{axid}({width}) - x_{axid}({x}))
                   .attr("height", y_{axid}({height}) - y_{axid}({y}));
    """

    def __init__(self, parent, ax, image, i=''):
        self._initialize(parent=parent, ax=ax, image=image)
        self.imageid = "{0}{1}".format(self.axid, i)

    def zoom(self):
        return self.IMAGE_ZOOM.format(imageid=self.imageid,
                                      axid=self.axid,
                                      x=self.x, y=self.y,
                                      width=self.width, height=self.height)

    def html(self):
        # import here in case people call matplotlib.use()
        from matplotlib.pyplot import imsave
        self.x, self.y = 0, 0
        data = self.image.get_array().data
        self.height, self.width = data.shape

        binary_buffer = io.BytesIO()
        imsave(binary_buffer, data)
        binary_buffer.seek(0)
        base64_data = base64.b64encode(binary_buffer.read())

        return self.IMAGE_TEMPLATE.format(axid=self.axid,
                                          imageid=self.imageid,
                                          base64_data=base64_data,
                                          x=self.x, y=self.y,
                                          width=self.width, height=self.height)
