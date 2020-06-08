import "../core/element";
import "path";

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
    dasharray: "none",
    alpha: 1.0,
    zorder: 2,
    drawstyle: "none"
};

function mpld3_Line(ax, props) {
    mpld3_PlotElement.call(this, ax, props);

    // Map line properties to path properties
    var pathProps = this.props;
    pathProps.facecolor = "none";
    pathProps.edgecolor = pathProps.color;
    delete pathProps.color;
    pathProps.edgewidth = pathProps.linewidth;
    delete pathProps.linewidth;

    const drawstyle = pathProps.drawstyle;
    delete pathProps.drawstyle;

    // Process path properties
    this.defaultProps = mpld3_Path.prototype.defaultProps;
    mpld3_Path.call(this, ax, pathProps);

    // Set interpolation type
    switch (drawstyle)
    {
       case "steps": //fallthrough
       case "steps-pre":
           this.datafunc = d3.line().curve(d3.curveStepBefore);
           break;
       case "steps-post":
           this.datafunc = d3.line().curve(d3.curveStepAfter);
           break;
       case "steps-mid":
           this.datafunc = d3.line().curve(d3.curveStep);
           break;
       default:
           this.datafunc = d3.line().curve(d3.curveLinear);
    }
}
