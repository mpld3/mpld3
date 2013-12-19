import abc
import warnings
from time import time

import numpy as np
from matplotlib.colors import colorConverter
from matplotlib.font_manager import FontProperties


def get_text_coordinates(txt):
    """Get figure coordinates of a text instance"""
    return txt.get_transform().transform(txt.get_position())


def color_to_hex(color):
    """Convert rgb tuple to hex color code"""
    rgb = colorConverter.to_rgb(color)
    return '#{:02X}{:02X}{:02X}'.format(*(int(255 * c) for c in rgb))


class D3Base(object):
    __metaclass__ = abc.ABCMeta

    def _initialize(self, parent=None, **kwds):
        self.parent = parent
        for key, val in kwds.items():
            setattr(self, key, val)

    @property
    def figid(self):
        if hasattr(self, '_figid'):
            return self._figid
        elif self.parent is not None and self.parent is not self:
            return self.parent.figid
        else:
            raise AttributeError("no attribute figid")

    @property
    def axid(self):
        if hasattr(self, '_axid'):
            return self._axid
        elif self.parent is not None and self.parent is not self:
            return self.parent.axid
        else:
            raise AttributeError("no attribute axid")

    @abc.abstractmethod
    def html(self):
        raise NotImplementedError()

    def style(self):
        return ''

    def __str__(self):
        return self.html()
        

class D3Figure(D3Base):
    D3_IMPORT = """
    <script type="text/javascript" src="http://d3js.org/d3.v3.min.js"></script>
    """

    STYLE = """
    <style>
    {styles}
    </style>
    """

    FIGURE_TEMPLATE = """
    <div id='figure{id}'></div>

    <script type="text/javascript">
    func{id} = function(figure){{

    var figwidth = {figwidth} * {dpi};
    var figheight = {figheight} * {dpi};

    var canvas = figure.append('svg:svg')
                   .attr('width', figwidth)
                   .attr('height', figheight)
                   .attr('class', 'canvas')

    {axes}

    }}

    // set a timeout of 0 to allow d3.js to load
    setTimeout(function(){{ func{id}(d3.select('#figure{id}')) }}, 0)
    </script>
    """
    def __init__(self, fig):
        # use time() to make sure multiple versions of this figure
        # don't cross-talk if used on the same page.
        self._initialize(parent=None, fig=fig)
        self._figid = str(id(self.fig)) + str(int(time()))
        self.axes = [D3Axes(self, ax, i + 1)
                     for i, ax in enumerate(fig.axes)]

    def style(self):
        return self.STYLE.format(styles='\n'.join([ax.style()
                                                   for ax in self.axes]))

    def html(self):
        axes = '\n'.join(map(str, self.axes))
        fig = self.FIGURE_TEMPLATE.format(id=self.figid,
                                          figwidth=self.fig.get_figwidth(),
                                          figheight=self.fig.get_figheight(),
                                          dpi=self.fig.dpi,
                                          axes=axes)
        return self.D3_IMPORT + self.style() + fig


class D3Axes(D3Base):
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

    AXES_TEMPLATE = """
    var axes_{axid} = canvas.append('g')
            .attr('transform', 'translate(' + ({bbox[0]} * figwidth) + ',' +
                                ((1 - {bbox[1]} - {bbox[3]}) * figheight) + ')')
            .attr('width', {bbox[2]} * figwidth)
            .attr('height', {bbox[3]} * figheight)
            .attr('class', 'main');

    // draw the x axis
    var x_{axid} = d3.scale.linear()
                       .domain([{xlim[0]}, {xlim[1]}])
                       .range([0, {bbox[2]} * figwidth]);

    var xAxis_{axid} = d3.svg.axis()
            .scale(x_{axid})
            .orient('bottom');

    axes_{axid}.append('g')
            .attr('transform', 'translate(0,' + {bbox[3]} * figheight + ')')
            .attr('class', 'axes{axid} x axis')
            .call(xAxis_{axid});

    // draw the y axis
    var y_{axid} = d3.scale.linear()
                       .domain([{ylim[0]}, {ylim[1]}])
                       .range([{bbox[3]} * figheight, 0]);

    var yAxis_{axid} = d3.svg.axis()
            .scale(y_{axid})
            .orient('left');

    axes_{axid}.append('g')
            .attr('transform', 'translate(0,0)')
            .attr('class', 'axes{axid} y axis')
            .call(yAxis_{axid});

    {elements}
    """
    def __init__(self, parent, ax, i):
        self._initialize(parent=parent, ax=ax)
        self._axid = str(i)
        self.lines = [D3Line2D(self, line, i + 1)
                      for i, line in enumerate(ax.lines)]
        self.texts = [D3Text(self, ax, text) for text in
                      ax.texts + [ax.xaxis.label, ax.yaxis.label, ax.title]]

        # Some warnings for pieces of matplotlib which are not yet implemented
        for attr in ['images', 'collections', 'containers',
                     'artists', 'patches', 'tables']:
            if len(getattr(ax, attr)) > 0:
                warnings.warn("{0} not implemented.  "
                              "Elements will be ignored".format(attr))

        if ax.legend_ is not None:
            warnings.warn("legend is not implemented: it will be ignored")

        if ax.xaxis._gridOnMajor or ax.yaxis._gridOnMajor:
            warnings.warn("grid is not implemented: it will be ignored")

    def style(self):
        xticks = self.ax.xaxis.get_ticklabels()
        if len(xticks) == 0:
            fontsize_x = 11
        else:
            fontsize_x = xticks[0].properties()['size']
        return '\n'.join([self.STYLE.format(axid=self.axid,
                                            figid=self.figid,
                                            fontsize=fontsize_x)] +
                         [l.style() for l in self.lines] +
                         [t.style() for t in self.texts])

    def html(self):
        elements = '\n'.join(map(str, self.lines + self.texts))
        xtick_size = self.ax.xaxis.get_major_ticks()[0].label.get_fontsize()
        ytick_size = self.ax.yaxis.get_major_ticks()[0].label.get_fontsize()

        return self.AXES_TEMPLATE.format(id=id(self.ax),
                                         axid=self.axid,
                                         xlim=self.ax.get_xlim(),
                                         ylim=self.ax.get_ylim(),
                                         xtick_size=xtick_size,
                                         ytick_size=ytick_size,
                                         bbox=self.ax.get_position().bounds,
                                         elements=elements)


class D3Line2D(D3Base):
    DATA_TEMPLATE = """
    var data_{lineid} = {data}
    """

    LINE_STYLE = """
    div#figure{figid}
    path.line{lineid} {{
        stroke: {linecolor};
        stroke-width: {linewidth};
        fill: none;
        stroke-opacity: {alpha};
    }}

    div#figure{figid}
    circle.points{lineid} {{
        stroke-width: {markeredgewidth};
        stroke: {markeredgecolor};
        fill: {markercolor};
        fill-opacity: {alpha};
        stroke-opacity: {alpha};
    }}
    """

    LINE_TEMPLATE = """
    var line_{lineid} = d3.svg.line()
         .x(function(d) {{return x_{axid}(d[0]);}})
         .y(function(d) {{return y_{axid}(d[1]);}})
         .interpolate("linear");

    axes_{axid}.append("svg:path")
                   .attr("d", line_{lineid}(data_{lineid}))
                   .attr('class', 'line{lineid}');
    """

    POINTS_TEMPLATE = """
    var g_{lineid} = axes_{axid}.append("svg:g");

    g_{lineid}.selectAll("scatter-dots-{lineid}")
          .data(data_{lineid})
          .enter().append("svg:circle")
              .attr("cx", function (d,i) {{ return x_{axid}(d[0]); }} )
              .attr("cy", function (d) {{ return y_{axid}(d[1]); }} )
              .attr("r", {markersize})
              .attr('class', 'points{lineid}');
    """
    def __init__(self, parent, line, i=''):
        self._initialize(parent=parent, line=line)
        self.lineid = "{0}{1}".format(self.axid, i)

    def style(self):
        alpha = self.line.get_alpha()
        if alpha is None:
            alpha = 1
        lc = color_to_hex(self.line.get_color())
        lw = self.line.get_linewidth()
        ms = 2. / 3. * self.line.get_markersize()
        mc = color_to_hex(self.line.get_markerfacecolor())
        mec = color_to_hex(self.line.get_markeredgecolor())
        mew = self.line.get_markeredgewidth()
        return self.LINE_STYLE.format(figid=self.figid,
                                      lineid=self.lineid,
                                      linecolor=lc,
                                      linewidth=lw,
                                      markersize=ms,
                                      markeredgewidth=mew,
                                      markeredgecolor=mec,
                                      markercolor=mc,
                                      alpha=alpha)
        
    def html(self):
        data = self.line.get_xydata().tolist()
        alpha = self.line.get_alpha()
        if alpha is None:
            alpha = 1
        marker = self.line.get_marker()
        style = self.line.get_linestyle()
        result = self.DATA_TEMPLATE.format(lineid=self.lineid, data=data)

        if marker not in ('None', 'none', None):
            # TODO: use actual marker, not simply circles
            if marker != 'o':
                warnings.warn("Only marker='o' is currently supported. "
                              "Defaulting to this.")

            ms = 2. / 3. * self.line.get_markersize()
            result += self.POINTS_TEMPLATE.format(lineid=self.lineid,
                                                  axid=self.axid,
                                                  markersize=ms,
                                                  data=data)
        if style not in ('None', 'none', None):
            # TODO: use actual line style
            if style not in ['-', 'solid']:
                warnings.warn("Only solid lines are currently supported. "
                              "Defaulting to this.")
            result += self.LINE_TEMPLATE.format(lineid=self.lineid,
                                                axid=self.axid,
                                                data=data)
        return result


class D3Text(D3Base):
    TEXT_TEMPLATE = """
    canvas.append("text")
        .text("{text}")
        .attr("class", "axes-text")
        .attr("x", {x})
        .attr("y", figheight - {y})
        .attr("font-size", "{fontsize}px")
        .attr("fill", "{color}")
        .attr("transform", "rotate({rotation},{x}," + (figheight - {y}) + ")")
        .attr("style", "text-anchor: {anchor};")
    """
    def __init__(self, parent, ax, text):
        self._initialize(parent=parent, ax=ax, text=text)
    
    def html(self):
        if not self.text.get_text():
            return ''
        
        x, y = get_text_coordinates(self.text)
        color =  color_to_hex(self.text.get_color())
        fontsize = self.text.get_size()

        # hack for y-label alignment
        # need to fix vertical/horizontal spacing
        if self.text is self.ax.yaxis.label:
            x += fontsize
            
        return self.TEXT_TEMPLATE.format(text=self.text.get_text(),
                                         x=x, y=y,
                                         fontsize=fontsize,
                                         color=color,
                                         rotation=-self.text.get_rotation(),
                                         anchor="middle")
