import "element";
import "../utils/";

/**********************************************************************/
/* Grid Object */
mpld3.Grid = mpld3_Grid;
mpld3_Grid.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Grid.prototype.constructor = mpld3_Grid;
mpld3_Grid.prototype.requiredProps = ["xy"];
mpld3_Grid.prototype.defaultProps = {
    color: "gray",
    dasharray: "2,2",
    alpha: "0.5",
    nticks: 10,
    gridOn: true,
    tickvalues: null,
    zorder: 0
};

function mpld3_Grid(ax, prop) {
    mpld3_PlotElement.call(this, ax, prop);
    this.cssclass = "mpld3-" + this.props.xy + "grid";

    if (this.props.xy == "x") {
        this.transform = "translate(0," + this.ax.height + ")";
        this.position = "bottom";
        this.scale = this.ax.xdom;
        this.tickSize = -this.ax.height;
    } else if (this.props.xy == "y") {
        this.transform = "translate(0,0)";
        this.position = "left";
        this.scale = this.ax.ydom;
        this.tickSize = -this.ax.width;
    } else {
        throw "unrecognized grid xy specifier: should be 'x' or 'y'";
    }
}

mpld3_Grid.prototype.draw = function() {
    var scaleMethod = {
        left: 'axisLeft',
        right: 'axisRight',
        top: 'axisTop',
        bottom: 'axisBottom',
    }[this.position];

    this.grid = d3[scaleMethod](this.scale)
        .ticks(this.props.nticks)
        .tickValues(this.props.tickvalues)
        .tickSize(this.tickSize, 0, 0)
        .tickFormat("");
    this.elem = this.ax.axes.append("g")
        .attr("class", this.cssclass)
        .attr("transform", this.transform)
        .call(this.grid);

    // We create header-level CSS to style these elements, because
    // zooming/panning creates new elements with these classes.
    mpld3.insert_css("div#" + this.ax.fig.figid +
        " ." + this.cssclass + " .tick", {
            "stroke": this.props.color,
            "stroke-dasharray": this.props.dasharray,
            "stroke-opacity": this.props.alpha
        });
    mpld3.insert_css("div#" + this.ax.fig.figid +
        " ." + this.cssclass + " path", {
            "stroke-width": 0
        });
    // Pass pointer events through so as not to break hovering.
    mpld3.insert_css("div#" + this.ax.fig.figid +
        " ." + this.cssclass + " .domain", {
            "pointer-events": "none"
        });
};

mpld3_Grid.prototype.zoomed = function(transform) {
    if (transform) {
        if (this.props.xy == 'x') {
            this.elem.call(this.grid.scale(transform.rescaleX(this.scale)));
        } else {
            this.elem.call(this.grid.scale(transform.rescaleY(this.scale)));
        }
    } else {
        // Backwards compatibility.
        this.elem.call(this.grid);
    }
};
