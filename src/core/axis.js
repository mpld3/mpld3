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
    minor_tickvalues: null,
    tickformat: null,
    minor_tickformat: null,
    filtered_tickvalues: null,
    filtered_tickformat: null,
    filtered_minortickvalues: null,
    filtered_minortickformat: null,
    tickformat_formatter: null,
    minor_tickformat_formatter: null,
    fontsize: "11px",
    fontcolor: "black",
    axiscolor: "black",
    scale: "linear",
    grid: {},
    minor_grid: {},
    minorticklength: null,
    majorticklength: null,
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
    this.minorTickFormat = null;
}

mpld3_Axis.prototype.getGrid = function(which) {
    which = which || 'major';
    this.filter_ticks(this.scale.domain());
    var isMinor = which === 'minor';
    var gridprop = {
        nticks: this.props.nticks,
        zorder: this.props.zorder,
        tickvalues: null,
        xy: this.props.xy
    }
    var gridstyle = isMinor ? this.props.minor_grid : this.props.grid;
    // NOTE: This could be simplified with ?? but our current uglify doesn't support it?
    var ticks = isMinor ? this.props.filtered_minortickvalues : this.props.filtered_tickvalues;
    if (ticks === null || ticks === undefined) {
        ticks = isMinor ? this.props.minor_tickvalues : this.props.tickvalues;
    }
    gridprop.tickvalues = ticks;
    if (gridstyle) {
        for (var key in gridstyle) {
            gridprop[key] = gridprop[key] || gridstyle[key];
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

function applyTickConfig(axisObj, values, formatterType, formatData, filteredFormat, tickFormatOverride, tickLength) {
    if (values) {
        axisObj = axisObj.tickValues(values);
    }
    if (tickLength !== undefined && tickLength !== null) {
        axisObj = axisObj.tickSize(tickLength, 0, 0);
    }
    if (formatData === "") {
        return axisObj.tickFormat(function() { return ""; });
    }
    if (formatterType == "index") {
        return axisObj.tickFormat(function(d, i) {
            return filteredFormat ? filteredFormat[d] : "";
        });
    } else if (formatterType == "percent" && formatData) {
        return axisObj.tickFormat(function(d, i) {
            var value = (d / formatData.xmax) * 100;
            var decimals = formatData.decimals || 0;
            var formatted_string = d3.format("." + decimals + "f")(value);
            return formatted_string + formatData.symbol;
        });
    } else if (formatterType == "str_method" && formatData) {
        return axisObj.tickFormat(function(d, i) {
            var formatted_string = d3.format(formatData.format_string)(d);
            return formatData.prefix + formatted_string + formatData.suffix;
        });
    } else if ((formatterType == "fixed" || formatterType == "func") && filteredFormat) {
        return axisObj.tickFormat(function(d, i) {
            return filteredFormat[i];
        });
    } else if (tickFormatOverride) {
        return axisObj.tickFormat(tickFormatOverride);
    }
    return axisObj;
}

mpld3_Axis.prototype.draw = function() {
    var scale = (this.props.xy === 'x') ?
        this.parent.props.xscale : this.parent.props.yscale;

    if (scale === 'date') {
        var domain = (this.props.xy === 'x') ?
            this.parent.x.domain() :
            this.parent.y.domain();
        var range = (this.props.xy === 'x') ?
            this.parent.xdom.domain() :
            this.parent.ydom.domain();
        var ordinal_to_js_date = d3.scaleLinear()
            .domain(domain)
            .range(range);

        var convertTicks = function(prop) {
            var values = this.props[prop];
            if (!values) return;
            this.props[prop] = values.map(function(value) {
                return new Date(ordinal_to_js_date(value));
            });
        }.bind(this);

        convertTicks('tickvalues');
        convertTicks('minor_tickvalues');
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

    if (this.tickNr) {
        this.axis = this.axis.ticks(this.tickNr);
    }

    // NOTE (@vladh): Since we're always using `filtered_tickvalues`, let's
    // always filter on the axes. Is this a good idea? Well, I hope so!
    this.axis = applyTickConfig(this.axis,
        this.props.filtered_tickvalues,
        this.props.tickformat_formatter,
        this.props.tickformat,
        this.props.filtered_tickformat,
        this.tickFormat,
        this.props.majorticklength || 3.5);

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

    if (this.props.filtered_minortickvalues && this.props.filtered_minortickvalues.length > 0) {
        this.minorAxis = d3[scaleMethod](this.scale);
        this.minorAxis = applyTickConfig(this.minorAxis,
            this.props.filtered_minortickvalues,
            this.props.minor_tickformat_formatter,
            this.props.minor_tickformat,
            this.props.filtered_minortickformat,
            this.minorTickFormat,
            this.props.minorticklength || 2);
        this.minorElem = this.ax.baseaxes.append('g')
            .attr("transform", this.transform)
            .attr("class", this.cssclass + " minor")
            .call(this.minorAxis);
    } else {
        this.minorAxis = null;
        this.minorElem = null;
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

    if (this.minorAxis) {
        this.minorAxis = this.minorAxis.tickValues(this.props.filtered_minortickvalues || []);
        if (transform) {
            if (this.props.xy == 'x') {
                this.minorElem.call(this.minorAxis.scale(transform.rescaleX(this.scale)));
            } else {
                this.minorElem.call(this.minorAxis.scale(transform.rescaleY(this.scale)));
            }
        } else {
            this.minorElem.call(this.minorAxis);
        }
    }
};

mpld3_Axis.prototype.setTicks = function(nr, format) {
    this.tickNr = nr;
    this.tickFormat = format;
};

mpld3_Axis.prototype.setMinorTicks = function(format) {
    this.minorTickFormat = format;
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

    if (this.props.minor_tickvalues) {
        const that = this;
        const minorFilteredTickIndices = this.props.minor_tickvalues.map(function(d, i) {
            return i;
        }).filter(function(d, i) {
            const v = that.props.minor_tickvalues[d];
            return (v >= domain[0]) && (v <= domain[1]);
        });
        this.props.filtered_minortickvalues = this.props.minor_tickvalues.filter(function(d, i) {
            return minorFilteredTickIndices.includes(i);
        });
        if (this.props.minor_tickformat) {
            this.props.filtered_minortickformat = this.props.minor_tickformat.filter(function(d, i) {
                return minorFilteredTickIndices.includes(i);
            });
        } else {
            this.props.filtered_minortickformat = this.props.minor_tickformat;
        }
    } else {
        this.props.filtered_minortickvalues = this.props.minor_tickvalues;
        this.props.filtered_minortickformat = this.props.minor_tickformat;
    }
}
