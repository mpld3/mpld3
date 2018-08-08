import "element";
import "grid";
import "../utils/";

/**********************************************************************/
/* Axis Object: */
mpld3.Axis = mpld3_Axis;
mpld3_Axis.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Axis.prototype.constructor = mpld3_Axis;
mpld3_Axis.prototype.requiredProps = ["position"];
mpld3_Axis.prototype.defaultProps = {
    nticks: 10,
    tickvalues: null,
    tickformat: null,
    fontsize: "11px",
    fontcolor: "black",
    axiscolor: "black",
    scale: "linear",
    grid: {},
    zorder: 0,
    visible: true
};

function mpld3_Axis(ax, props) {
    mpld3_PlotElement.call(this, ax, props);

    var trans = {
        bottom: [0, this.ax.height],
        top: [0, 0],
        left: [0, 0],
        right: [this.ax.width, 0]
    };
    var xy = {
        bottom: 'x',
        top: 'x',
        left: 'y',
        right: 'y'
    }

    this.transform = "translate(" + trans[this.props.position] + ")";
    this.props.xy = xy[this.props.position];
    this.cssclass = "mpld3-" + this.props.xy + "axis";
    this.scale = this.ax[this.props.xy + "dom"];

    this.tickNr = null;
    this.tickFormat = null;
}

mpld3_Axis.prototype.getGrid = function() {
    var gridprop = {
        nticks: this.props.nticks,
        zorder: this.props.zorder,
        tickvalues: this.props.tickvalues,
        xy: this.props.xy
    }
    if (this.props.grid) {
        for (var key in this.props.grid) {
            gridprop[key] = this.props.grid[key];
        }
    }
    return new mpld3_Grid(this.ax, gridprop);
};

mpld3_Axis.prototype.draw = function() {
    /*
    Wraps text in a certain element.
    @param text {Element} The text element.
    @param width {Number} Maximum width in pixels.
    @param lineHeight {Number=1.1} Height of a line in percentage, so 1.1 is 110% line height.
    */
    function wrap(text, width, lineHeight) {
        lineHeight = lineHeight || 1.2;
        text.each(function() {
            var text = d3.select(this);
            var bbox = text.node().getBBox();
            var textHeight = bbox.height;
            var words = text.text().split(/\s+/).reverse();
            var word;
            var line = [];
            var lineNumber = 0;
            var y = text.attr('y');
            var dy = textHeight;
            var tspan = text
                .text(null)
                .append('tspan')
                .attr('x', 0)
                .attr('y', y)
                .attr('dy', dy);
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(' '));
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(' '));
                    line = [word];
                    tspan = text
                        .append('tspan')
                        .attr('x', 0)
                        .attr('y', y)
                        .attr('dy', (++lineNumber * (textHeight * lineHeight)) + dy)
                        .text(word);
                }
            }
        })
    }

    var TEXT_WIDTH = 80;

    var scale = (this.props.xy === 'x') ?
        this.parent.props.xscale : this.parent.props.yscale;

    if (scale === 'date' && this.props.tickvalues) {
        // Convert tick locations from floating point ordinal values
        // to JavaScript Dates
        var domain = (this.props.xy === 'x') ?
            this.parent.x.domain() :
            this.parent.y.domain();
        var range = (this.props.xy === 'x') ?
            this.parent.xdom.domain() :
            this.parent.ydom.domain();
        var ordinal_to_js_date = d3.scaleLinear()
            .domain(domain)
            .range(range);
        this.props.tickvalues = this.props.tickvalues.map(function(value) {
            return new Date(ordinal_to_js_date(value));
        });
    }

    var scaleMethod = {
        left: 'axisLeft',
        right: 'axisRight',
        top: 'axisTop',
        bottom: 'axisBottom',
    }[this.props.position];

    this.axis = d3[scaleMethod](this.scale);

    if (this.props.tickformat && this.props.tickvalues) {
        this.axis = this.axis
            .tickValues(this.props.tickvalues)
            .tickFormat(function(d, i) { return this.props.tickformat[i] }.bind(this));
    } else {
        if (this.tickNr) {
            this.axis = this.axis.ticks(this.tickNr);
        }
        if (this.tickFormat) {
            this.axis = this.axis.tickFormat(this.tickFormat);
        }
    }

    this.filter_ticks(this.axis.tickValues, this.axis.scale().domain());

// good tips: http://bl.ocks.org/mbostock/3048166 in response to http://stackoverflow.com/questions/11286872/how-do-i-make-a-custom-axis-formatter-for-hours-minutes-in-d3-js

    this.elem = this.ax.baseaxes.append('g')
        .attr("transform", this.transform)
        .attr("class", this.cssclass)
        .call(this.axis);

    if (this.props.xy == 'x') {
        this.elem.selectAll('text').call(wrap, TEXT_WIDTH);
    }

    // We create header-level CSS to style these elements, because
    // zooming/panning creates new elements with these classes.
    mpld3.insert_css("div#" + this.ax.fig.figid + " ." + this.cssclass + " line, " + " ." + this.cssclass + " path", {
        "shape-rendering": "crispEdges",
        "stroke": this.props.axiscolor,
        "fill": "none"
    });
    mpld3.insert_css("div#" + this.ax.fig.figid + " ." + this.cssclass + " text", {
        "font-family": "sans-serif",
        "font-size": this.props.fontsize + "px",
        "fill": this.props.fontcolor,
        "stroke": "none"
    });
};

mpld3_Axis.prototype.zoomed = function(transform) {
    // if we set tickValues for the axis, we are responsible for
    // updating them when they pan or zoom off of the chart
    // this.filter_ticks(this.axis.tickValues, this.axis.scale().domain());
    if (transform) {
        if (this.props.xy == 'x') {
            this.elem.call(this.axis.scale(transform.rescaleX(this.scale)));
        } else {
            this.elem.call(this.axis.scale(transform.rescaleY(this.scale)));
        }
    } else {
        this.elem.call(this.axis);
    }
};

mpld3_Axis.prototype.setTicks = function(nr, format) {
    this.tickNr = nr;
    this.tickFormat = format;
};

mpld3_Axis.prototype.filter_ticks = function(tickValues, domain) {
    //Remove ticks outside axis limits.
    if (this.props.tickvalues != null) {
        tickValues(this.props.tickvalues.filter(
            function (v) { return (v >= domain[0]) && (v <= domain[1]); }));
    }
}
