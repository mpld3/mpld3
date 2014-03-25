import "core";

/**********************************************************************/
/* Line Element: inherits from mpld3.Path */
mpld3.Line = mpld3_Line;
mpld3_Line.prototype = Object.create(mpld3_Path.prototype);
mpld3_Line.prototype.constructor = mpld3_Line;
mpld3_Line.prototype.requiredProps = ["data"];
mpld3_Line.prototype.defaultProps = {
    xindex: 0,
    yindex: 1,
    coordinates: "data",
    color: "salmon",
    linewidth: 2,
    dasharray: "10,0",
    alpha: 1.0,
    zorder: 2
};

function mpld3_Line(ax, props) {
    mpld3_PlotElement.call(this, ax, props);

    // Map line properties to path properties
    pathProps = this.props;
    pathProps.facecolor = "none";
    pathProps.edgecolor = pathProps.color;
    delete pathProps.color;
    pathProps.edgewidth = pathProps.linewidth;
    delete pathProps.linewidth;

    // Process path properties
    this.defaultProps = mpld3_Path.prototype.defaultProps;
    mpld3_Path.call(this, ax, pathProps);

    // This is optional, but is more efficient than relying on path
    this.datafunc = d3.svg.line().interpolate("linear");
}