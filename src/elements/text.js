/**********************************************************************/
/* Text Element */
mpld3.Text = mpld3_Text;
mpld3_Text.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Text.prototype.constructor = mpld3_Text;
mpld3_Text.prototype.requiredProps = ["text", "position"];
mpld3_Text.prototype.defaultProps = {
    coordinates: "data",
    h_anchor: "start",
    v_baseline: "auto",
    rotation: 0,
    fontsize: 11,
    drawstyle: "none",
    color: "black",
    alpha: 1.0,
    zorder: 3
};

function mpld3_Text(ax, props) {
    mpld3_PlotElement.call(this, ax, props);
    this.text = this.props.text;
    this.position = this.props.position;
    this.coords = new mpld3_Coordinates(this.props.coordinates, this.ax);
};

mpld3_Text.prototype.draw = function() {
    if (this.props.coordinates == "data") {
        if (this.coords.zoomable) {
            this.obj = this.ax.paths.append("text");
        } else {
            this.obj = this.ax.staticPaths.append("text");
        }
    } else {
        this.obj = this.ax.baseaxes.append("text");
    }

    this.obj
        .attr("class", "mpld3-text")
        .attr("xml:space", "preserve")
        .text(this.text)
        .style("text-anchor", this.props.h_anchor)
        .style("dominant-baseline", this.props.v_baseline)
        .style("font-size", this.props.fontsize)
        .style("fill", this.props.color)
        .style("opacity", this.props.alpha);
    this.applyTransform();
};

mpld3_Text.prototype.elements = function(d) {
    return d3.select(this.obj);
};

mpld3_Text.prototype.applyTransform = function(zoomScale) {
    var pos = this.coords.xy(this.position);
    var transform = "";
    this.obj.attr("x", pos[0]).attr("y", pos[1]);

    // Keep glyphs at their original size within the zoomed data layer.
    // Scaling around the text anchor preserves its data position and zorder.
    if (zoomScale && zoomScale !== 1)
        transform = "translate(" + pos + ")scale(" + (1 / zoomScale) +
            ")translate(" + [-pos[0], -pos[1]] + ")";
    if (this.props.rotation)
        transform += "rotate(" + this.props.rotation + "," + pos + ")";
    this.obj.attr("transform", transform || null);
}

mpld3_Text.prototype.zoomed = function(transform) {
    if (this.coords.zoomable)
        this.applyTransform(transform.k);
};
