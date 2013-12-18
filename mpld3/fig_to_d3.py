import numpy as np
from matplotlib.colors import colorConverter


D3_FIGURE = """
<script type="text/javascript" src="http://d3js.org/d3.v3.min.js"></script>

<style>
.axis line, .axis path {{
    shape-rendering: crispEdges;
    stroke: black;
    fill: none;
}}

.axis text {{
    font-family: sans-serif;
    font-size: 11px;
}}

</style>

<div id='chart{id}'></div>

<script type="text/javascript">
// set a timeout of 0 to make sure d3.js is loaded
setTimeout(function(){{
var figwidth = {figwidth} * {dpi};
var figheight = {figheight} * {dpi};

var chart_{id} = d3.select('#chart{id}')
                   .append('svg:svg')
                   .attr('width', figwidth)
                   .attr('height', figheight)
                   .attr('class', 'chart');

{axes}
}}, 0)
</script>
"""


D3_AXES = """
var axes_{id} = chart_{figid}.append('g')
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
	.attr('class', 'main axis')
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
	.attr('class', 'main axis')
	.call(yAxis_{id});

{elements}
"""

D3_LINE = """
var data_{id} = {data}

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


D3_PTS = """
var g_{id} = axes_{axid}.append("svg:g");

var data_{id} = {data};
    
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

D3_TEXT = """
chart_{figid}.append("text")
    .text("{text}")
    .attr("class", "axes-text")
    .attr("x", {x})
    .attr("y", figheight - {y})
    .attr("font-size", "{fontsize}px")
    .attr("fill", "{color}")
    .attr("transform", "rotate({rotation},{x}," + (figheight - {y}) + ")")
    .attr("style", "text-anchor: {anchor};")
"""


def get_text_coordinates(txt):
    """Get figure coordinates of a text instance"""
    return txt.get_transform().transform(txt.get_position())


def color_to_hex(color):
    """Convert rgb tuple to hex color code"""
    rgb = colorConverter.to_rgb(color)
    return '#{:02X}{:02X}{:02X}'.format(*(int(255 * c) for c in rgb))


def fig_to_d3(fig):
    """Output d3 representation of the figure"""
    figheight = fig.get_figheight()
    figwidth = fig.get_figwidth()

    axes_html = []

    for ax in fig.axes:
        bounds = ax.get_position().bounds

        axes_elements = []

        for i, line in enumerate(ax.lines):
            data = line.get_xydata().tolist()
            alpha = line.get_alpha()
            if alpha is None:
                alpha = 1
            marker = line.get_marker()
            style = line.get_linestyle()

            if marker not in ('None', 'none', None):
                # TODO: use actual marker, not simply circles
                ms = 2. / 3. * line.get_markersize()
                mc = color_to_hex(line.get_markerfacecolor())
                mec = color_to_hex(line.get_markeredgecolor())
                mew = line.get_markeredgewidth()
            
                axes_elements.append(D3_PTS.format(id=id(line),
                                                   axid=id(ax),
                                                   i=i + 1,
                                                   data=data,
                                                   markersize=ms,
                                                   markercolor=mc,
                                                   markeredgecolor=mec,
                                                   markeredgewidth=mew,
                                                   alpha=alpha))

            if style not in ('None', 'none', None):
                # TODO: use actual line style
                lc = color_to_hex(line.get_color())
                lw = line.get_linewidth()
                axes_elements.append(D3_LINE.format(id=id(line),
                                                    axid=id(ax),
                                                    figid=id(fig),
                                                    data=data,
                                                    linecolor=lc,
                                                    linewidth=lw,
                                                    alpha=alpha))
                

        texts = ax.texts + [ax.xaxis.label, ax.yaxis.label, ax.title]
        for text in texts:
            if not text.get_text():
                continue
            x, y = get_text_coordinates(text)
            color =  color_to_hex(colorConverter.to_rgb(text.get_color()))
            fontsize = text.get_size()

            # hack for y-label alignment
            if text is ax.yaxis.label:
                x += fontsize
            
            axes_elements.append(D3_TEXT.format(figid=id(fig),
                                                text=text.get_text(),
                                                x=x, y=y,
                                                fontsize=fontsize,
                                                color=color,
                                                rotation=-text.get_rotation(),
                                                anchor="middle"))
                                             
        xtick_size = ax.xaxis.get_major_ticks()[0].label.get_fontsize()
        ytick_size = ax.yaxis.get_major_ticks()[0].label.get_fontsize()

        axes_html.append(D3_AXES.format(id=id(ax),
                                        figid=id(fig),
                                        xlim=ax.get_xlim(),
                                        ylim=ax.get_ylim(),
                                        xtick_size=xtick_size,
                                        ytick_size=ytick_size,
                                        bbox=ax.get_position().bounds,
                                        elements='\n'.join(axes_elements)))
                             
    fig_html = D3_FIGURE.format(id=id(fig),
                                figwidth=fig.get_figwidth(),
                                figheight=fig.get_figheight(),
                                dpi=fig.dpi,
                                axes='\n'.join(axes_html))

    return fig_html
                         
                         

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(np.random.random(10),
            np.random.random(10),
            'og')
    ax.plot(np.linspace(0.1, 0.9, 10),
            np.random.random(10), '-b', lw=5, alpha=0.2)
    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_title('title')
    
    open('tmp.html', 'w').write(fig_to_d3(fig))

    #plt.show()
