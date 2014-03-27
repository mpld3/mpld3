import "../core/element";
import "../core/coordinates";
import "../utils/";

/**********************************************************************/
/* Path Element */
mpld3.Path = mpld3_Path;
mpld3_Path.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Path.prototype.constructor = mpld3_Path;
mpld3_Path.prototype.requiredProps = ["data"];
mpld3_Path.prototype.defaultProps = {
    xindex: 0,
    yindex: 1,
    coordinates: "data",
    facecolor: "green",
    edgecolor: "black",
    edgewidth: 1,
    dasharray: "10,0",
    pathcodes: null,
    offset: null,
    offsetcoordinates: "data",
    alpha: 1.0,
    zorder: 1
};

function mpld3_Path(ax, props) {
    mpld3_PlotElement.call(this, ax, props);
    this.data = ax.fig.get_data(this.props.data);
    this.pathcodes = this.props.pathcodes;

    this.pathcoords = new mpld3_Coordinates(this.props.coordinates,
        this.ax);
    this.offsetcoords = new mpld3_Coordinates(this.props.offsetcoordinates,
        this.ax);
    this.datafunc = mpld3_path();
}

mpld3_Path.prototype.nanFilter = function(d, i) {
    return (!isNaN(d[this.props.xindex]) && !isNaN(d[this.props.yindex]));
};

mpld3_Path.prototype.draw = function() {
    this.datafunc
        .defined(this.nanFilter.bind(this))
        .x(function(d) {
            return this.pathcoords.x(d[this.props.xindex]);
        })
        .y(function(d) {
            return this.pathcoords.y(d[this.props.yindex]);
        });

    this.path = this.ax.axes.append("svg:path")
        .attr("d", this.datafunc(this.data, this.pathcodes))
        .attr('class', "mpld3-path")
        .style("stroke", this.props.edgecolor)
        .style("stroke-width", this.props.edgewidth)
        .style("stroke-dasharray", this.props.dasharray)
        .style("stroke-opacity", this.props.alpha)
        .style("fill", this.props.facecolor)
        .style("fill-opacity", this.props.alpha)
        .attr("vector-effect", "non-scaling-stroke");

    if (this.props.offset !== null) {
        var offset = this.offsetcoords.xy(this.props.offset);
        this.path.attr("transform", "translate(" + offset + ")");
    }
};

mpld3_Path.prototype.elements = function(d) {
    return this.path;
};

mpld3_Path.prototype.zoomed = function() {
    if (this.pathcoords.zoomable) {
        this.path.attr("d", this.datafunc(this.data, this.pathcodes));
    }
    if (this.props.offset !== null && this.offsetcoords.zoomable) {
        var offset = this.offsetcoords.xy(this.props.offset);
        this.path.attr("transform", "translate(" + offset + ")");
    }
};
