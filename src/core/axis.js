import "element";
import "grid";
import "../utils/";

/**********************************************************************/
/* Axis Object: */
/**
 * Props:
 * `tickformat_formatter`: the variable comes from `mpld3/mplextractor` and
 *  defines which has been used. Depending on the class used different `tickformat` will be supplied.
 *  The variables include:
 *    - `percent`     = matplotlib.ticker.PercentFormatter
 *    - `index`       = matplotlib.ticker.IndexFormatter
 *    - `fixed`       = matplotlib.ticker.FixedFormatter
 *    - `str_method`  = matplotlib.ticker.StrMethodFormatter
 *
 * `tickformat`: the variable comes from `mpld3/mplextractor` and defines
 * the variables inside of each `matplotlib.ticker`. The variable inside this changes
 * depending on `tickformat_formatter` used.
 *    - tickformat_formatter: `percent`
 *      tickformat: {
 *        "xmax": formatter.xmax,
 *        "decimals": formatter.decimals,
 *        "symbol": formatter.symbol,
 *      } <- variables defined in matplotlib.ticker.PercentFormatter
 *    - tickformat_formatter: `index`
 *      tickformat: [...] <- array of ticks e.g. ["a", "b", "c"]
 *    - tickformat_formatter: `fixed`
 *      tickformat: [...] <- array of ticks e.g. ["a", "b", "c"] similar to `index`
 *    - tickformat_formatter: `str_method`
 *      tickformat: "..." <- format accepted by https://github.com/d3/d3-format
 *
 * `tickvalue`: values from `ticker.FixedLocator` if set the axis lables will become fixed and
 * will not scale
 *
 **/

mpld3.Axis = mpld3_Axis;
mpld3_Axis.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Axis.prototype.constructor = mpld3_Axis;
mpld3_Axis.prototype.requiredProps = ["position"];
mpld3_Axis.prototype.defaultProps = {
    nticks: 10,
    tickvalues: null,
    tickformat: null,
    filtered_tickvalues: null,
    filtered_tickformat: null,
    tickformat_formatter: null,
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

    this.ax = ax;
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
        tickvalues: null,
        xy: this.props.xy
    }
    if (this.props.grid) {
        for (var key in this.props.grid) {
            gridprop[key] = this.props.grid[key];
        }
    }
    return new mpld3_Grid(this.ax, gridprop);
};

mpld3_Axis.prototype.wrapTicks = function() {
    /*
    Wraps text in a certain element.
    @param text {Element} The text element.
    @param width {Number} Maximum width in pixels.
    @param lineHeight {Number=1.2} Height of a line in percentage, so 1.2 is 120% line height.
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

    if (this.props.xy == 'x') {
        this.elem.selectAll('text').call(wrap, TEXT_WIDTH);
    }
};

mpld3_Axis.prototype.draw = function() {
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

    var that = this;

    this.filter_ticks(this.axis.scale().domain());

    if (this.props.tickformat_formatter == "index") {
        this.axis = this.axis.tickFormat(function(d, i) {
            return that.props.filtered_tickformat[d];
        });
    } else if (this.props.tickformat_formatter == "percent") {
        this.axis = this.axis.tickFormat(function(d, i) {
            var value = (d / that.props.tickformat.xmax) * 100;
            var decimals = that.props.tickformat.decimals || 0;
            var formatted_string = d3.format("."+decimals+"f")(value);
            return formatted_string + that.props.tickformat.symbol;
        });
    } else if (this.props.tickformat_formatter == "str_method") {
        this.axis = this.axis.tickFormat(function(d, i) {
            var formatted_string = d3.format(that.props.tickformat.format_string)(d);
            return that.props.tickformat.prefix + formatted_string + that.props.tickformat.suffix;
        });
    } else if (this.props.tickformat_formatter == "fixed") {
        this.axis = this.axis.tickFormat(function(d, i) {
            return that.props.filtered_tickformat[i];
        });
    } else if (this.tickFormat) {
        this.axis = this.axis.tickFormat(this.tickFormat);
    }

    if (this.tickNr) {
        this.axis = this.axis.ticks(this.tickNr);
    }

    // NOTE (@vladh): Since we're always using `filtered_tickvalues`, let's
    // always filter on the axes. Is this a good idea? Well, I hope so!
    this.axis = this.axis.tickValues(this.props.filtered_tickvalues)

    /*
    Good tips:
    http://bl.ocks.org/mbostock/3048166
    in response to
    http://stackoverflow.com/questions/11286872/how-do-i-make-a-custom-axis-formatter-for-hours-minutes-in-d3-js
    */

    this.elem = this.ax.baseaxes.append('g')
        .attr("transform", this.transform)
        .attr("class", this.cssclass)
        .call(this.axis);

    this.wrapTicks();

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
    this.filter_ticks(this.axis.scale().domain());
    this.axis = this.axis.tickValues(this.props.filtered_tickvalues)
    if (transform) {
        if (this.props.xy == 'x') {
            this.elem.call(this.axis.scale(transform.rescaleX(this.scale)));
        } else {
            this.elem.call(this.axis.scale(transform.rescaleY(this.scale)));
        }
        this.wrapTicks();
    } else {
        this.elem.call(this.axis);
    }
};

mpld3_Axis.prototype.setTicks = function(nr, format) {
    this.tickNr = nr;
    this.tickFormat = format;
};

mpld3_Axis.prototype.filter_ticks = function(domain) {
    //Remove ticks outside axis limits.
    if (this.props.tickvalues) {
        const that = this;
        const filteredTickIndices = this.props.tickvalues.map(function(d, i) {
            return i;
        }).filter(function(d, i) {
            const v = that.props.tickvalues[d];
            return (v >= domain[0]) && (v <= domain[1]);
        });
        this.props.filtered_tickvalues = this.props.tickvalues.filter(function(d, i) {
            return filteredTickIndices.includes(i);
        });
        if (this.props.tickformat) {
            this.props.filtered_tickformat = this.props.tickformat.filter(function(d, i) {
                return filteredTickIndices.includes(i);
            });
        } else {
            this.props.filtered_tickformat = this.props.tickformat;
        }
    } else {
        this.props.filtered_tickvalues = this.props.tickvalues;
        this.props.filtered_tickformat = this.props.tickformat;
    }
}
