import abc
import numpy as np
from time import time
from matplotlib.colors import colorConverter


def get_text_coordinates(txt):
    """Get figure coordinates of a text instance"""
    return txt.get_transform().transform(txt.get_position())


def color_to_hex(color):
    """Convert rgb tuple to hex color code"""
    rgb = colorConverter.to_rgb(color)
    return '#{:02X}{:02X}{:02X}'.format(*(int(255 * c) for c in rgb))


class D3Base(object):
    __metaclass__ = abc.ABCMeta

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
    <div id='chart{id}'></div>

    <script type="text/javascript">
    func{id} = function(chart){{

    var figwidth = {figwidth} * {dpi};
    var figheight = {figheight} * {dpi};

    chart = chart.append('svg:svg')
                   .attr('width', figwidth)
                   .attr('height', figheight)
                   .attr('class', chart)

    {axes}

    }}

    // set a timeout of 0 to allow d3.js to load
    setTimeout(function(){{ func{id}(d3.select('#chart{id}')) }}, 0)
    </script>
    """
    def __init__(self, fig):
        # use time() to make sure multiple versions of this figure
        # don't cross-talk if used on the same page.
        self.fig = fig
        self.axes = [D3Axes(ax, i + 1)
                     for i, ax in enumerate(fig.axes)]

    def style(self):
        return self.STYLE.format(styles='\n'.join([ax.style()
                                                   for ax in self.axes]))

    def html(self):
        axes = '\n'.join(map(str, self.axes))
        fig_id = str(id(self.fig)) + str(int(time()))
        fig = self.FIGURE_TEMPLATE.format(id=fig_id,
                                          figwidth=self.fig.get_figwidth(),
                                          figheight=self.fig.get_figheight(),
                                          dpi=self.fig.dpi,
                                          axes=axes)
        return self.D3_IMPORT + self.style() + fig


class D3Axes(D3Base):
    STYLE = """
    .axes{i}.axis line, .axes{i}.axis path {{
        shape-rendering: crispEdges;
        stroke: black;
        fill: none;
    }}

    .axes{i}.axis text {{
        font-family: sans-serif;
        font-size: {fontsize}px;
    }}
    """

    AXES_TEMPLATE = """
    var axes_{id} = chart.append('g')
            .attr('transform', 'translate(' + ({bbox[0]} * figwidth) + ',' +
                                ((1 - {bbox[1]} - {bbox[3]}) * figheight) + ')')
            .attr('width', {bbox[2]} * figwidth)
            .attr('height', {bbox[3]} * figheight)
            .attr('class', 'main');

    // draw the x axis
    var x_{id} = d3.scale.linear()
                       .domain([{xlim[0]}, {xlim[1]}])
                       .range([0, {bbox[2]} * figwidth]);

    var xAxis_{id} = d3.svg.axis()
            .scale(x_{id})
            .orient('bottom');

    axes_{id}.append('g')
            .attr('transform', 'translate(0,' + {bbox[3]} * figheight + ')')
            .attr('class', 'axes{i} x axis')
            .call(xAxis_{id});

    // draw the y axis
    var y_{id} = d3.scale.linear()
                       .domain([{ylim[0]}, {ylim[1]}])
                       .range([{bbox[3]} * figheight, 0]);

    var yAxis_{id} = d3.svg.axis()
            .scale(y_{id})
            .orient('left');

    axes_{id}.append('g')
            .attr('transform', 'translate(0,0)')
            .attr('class', 'axes{i} y axis')
            .call(yAxis_{id});

    {elements}
    """
    def __init__(self, ax, i):
        self.ax = ax
        self.i = i
        self.lines = [D3Line2D(ax, line, i + 1)
                      for i, line in enumerate(ax.lines)]
        self.texts = [D3Text(ax, text) for text in
                      ax.texts + [ax.xaxis.label, ax.yaxis.label, ax.title]]

    def style(self):
        return '\n'.join([self.STYLE.format(i=self.i,
                                            fontsize=11)] +
                         [l.style() for l in self.lines] +
                         [t.style() for t in self.texts])

    def html(self):
        elements = '\n'.join(map(str, self.lines + self.texts))
        xtick_size = self.ax.xaxis.get_major_ticks()[0].label.get_fontsize()
        ytick_size = self.ax.yaxis.get_major_ticks()[0].label.get_fontsize()

        return self.AXES_TEMPLATE.format(id=id(self.ax),
                                         i=self.i,
                                         xlim=self.ax.get_xlim(),
                                         ylim=self.ax.get_ylim(),
                                         xtick_size=xtick_size,
                                         ytick_size=ytick_size,
                                         bbox=self.ax.get_position().bounds,
                                         elements=elements)


class D3Line2D(D3Base):
    DATA_TEMPLATE = """
    var data_{id} = {data}
    """

    LINE_TEMPLATE = """
    var line_{id} = d3.svg.line()
         .x(function(d) {{return x_{axid}(d[0]);}})
         .y(function(d) {{return y_{axid}(d[1]);}})
         .interpolate("linear");

    axes_{axid}.append("svg:path")
                  .attr("d", line_{id}(data_{id}))
                  .attr("stroke", "{linecolor}")
                  .attr("stroke-width", {linewidth})
                  .attr("fill", "none")
                  .attr("stroke-opacity", {alpha})
    """

    POINTS_TEMPLATE = """
    var g_{id} = axes_{axid}.append("svg:g");

    g_{id}.selectAll("scatter-dots-{i}")
          .data(data_{id})
          .enter().append("svg:circle")
              .attr("cx", function (d,i) {{ return x_{axid}(d[0]); }} )
              .attr("cy", function (d) {{ return y_{axid}(d[1]); }} )
              .attr("r", {markersize})
              .attr("stroke-width", {markeredgewidth})
              .attr("stroke", "{markeredgecolor}")
              .attr("fill", "{markercolor}")
              .attr("fill-opacity", {alpha})
              .attr("stroke-opacity", {alpha});
    """
    def __init__(self, ax, line, i=''):
        self.ax = ax
        self.line = line
        self.i = i
        
    def html(self):
        data = self.line.get_xydata().tolist()
        alpha = self.line.get_alpha()
        if alpha is None:
            alpha = 1
        marker = self.line.get_marker()
        style = self.line.get_linestyle()
        result = self.DATA_TEMPLATE.format(id=id(self.line), data=data)

        if marker not in ('None', 'none', None):
            # TODO: use actual marker, not simply circles
            ms = 2. / 3. * self.line.get_markersize()
            mc = color_to_hex(self.line.get_markerfacecolor())
            mec = color_to_hex(self.line.get_markeredgecolor())
            mew = self.line.get_markeredgewidth()
            result += self.POINTS_TEMPLATE.format(id=id(self.line),
                                                  axid=id(self.ax),
                                                  i=self.i,
                                                  data=data,
                                                  markersize=ms,
                                                  markercolor=mc,
                                                  markeredgecolor=mec,
                                                  markeredgewidth=mew,
                                                  alpha=alpha)
        if style not in ('None', 'none', None):
            # TODO: use actual line style
            lc = color_to_hex(self.line.get_color())
            lw = self.line.get_linewidth()
            result += self.LINE_TEMPLATE.format(id=id(self.line),
                                                axid=id(self.ax),
                                                figid=id(self.ax.figure),
                                                data=data,
                                                linecolor=lc,
                                                linewidth=lw,
                                                alpha=alpha)
        return result


class D3Text(D3Base):
    TEXT_TEMPLATE = """
    chart.append("text")
        .text("{text}")
        .attr("class", "axes-text")
        .attr("x", {x})
        .attr("y", figheight - {y})
        .attr("font-size", "{fontsize}px")
        .attr("fill", "{color}")
        .attr("transform", "rotate({rotation},{x}," + (figheight - {y}) + ")")
        .attr("style", "text-anchor: {anchor};")
    """
    def __init__(self, ax, text):
        self.ax = ax
        self.text = text
    
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
