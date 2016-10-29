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
    zorder: 0
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
        var ordinal_to_js_date = d3.scale.linear()
            .domain(domain)
            .range(range);
        this.props.tickvalues = this.props.tickvalues.map(function(value) {
            return new Date(ordinal_to_js_date(value));
        });
    }

    var tickformat = mpld3_tickFormat(this.props.tickformat, this.props.tickvalues);

    this.axis = d3.svg.axis()
        .scale(this.scale)
        .orient(this.props.position)
        .ticks(this.props.nticks)
        .tickValues(this.props.tickvalues)
        .tickFormat(tickformat);

    this.filter_ticks(this.axis.tickValues, this.axis.scale().domain());

// good tips: http://bl.ocks.org/mbostock/3048166 in response to http://stackoverflow.com/questions/11286872/how-do-i-make-a-custom-axis-formatter-for-hours-minutes-in-d3-js

    this.elem = this.ax.baseaxes.append('g')
        .attr("transform", this.transform)
        .attr("class", this.cssclass)
        .call(this.axis);

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

function mpld3_tickFormat(tickformat, tickvalues) {
    if (tickformat === "" || tickformat === null) {
        return tickformat;
    }
    else {
        // tickvalues is an array of tick locations
        // tickformat is an array of tick labels
        return d3.scale.threshold()
            .domain(tickvalues.slice(1))
            .range(tickformat);
    }
}

mpld3_Axis.prototype.zoomed = function() {
    // if we set tickValues for the axis, we are responsible for
    // updating them when they pan or zoom off of the chart
    this.filter_ticks(this.axis.tickValues, this.axis.scale().domain());
    this.elem.call(this.axis);
};

mpld3_Axis.prototype.filter_ticks = function(tickValues, domain) {
    //Remove ticks outside axis limits.
    if (this.props.tickvalues != null) {
        tickValues(this.props.tickvalues.filter(
            function (v) { return (v >= domain[0]) && (v <= domain[1]); }));
    }
}
