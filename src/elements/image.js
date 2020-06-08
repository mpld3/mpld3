/**********************************************************************/
/* Image Object */
mpld3.Image = mpld3_Image;
mpld3_Image.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Image.prototype.constructor = mpld3_Image;
mpld3_Image.prototype.requiredProps = ["data", "extent"];
mpld3_Image.prototype.defaultProps = {
    alpha: 1.0,
    coordinates: "data",
    drawstyle: "none",
    zorder: 1
};

function mpld3_Image(ax, props) {
    mpld3_PlotElement.call(this, ax, props);
    this.coords = new mpld3_Coordinates(this.props.coordinates, this.ax);
}

mpld3_Image.prototype.draw = function() {
    this.image = this.ax.paths.append("svg:image")

    this.image = this.image
        .attr('class', 'mpld3-image')
        .attr('xlink:href', "data:image/png;base64," + this.props.data)
        .style('opacity', this.props.alpha)
        .attr("preserveAspectRatio", "none");
    this.updateDimensions();
};

mpld3_Image.prototype.elements = function(d) {
    return d3.select(this.image);
};

mpld3_Image.prototype.updateDimensions = function() {
    var extent = this.props.extent;
    this.image
        .attr("x", this.coords.x(extent[0]))
        .attr("y", this.coords.y(extent[3]))
        .attr("width", this.coords.x(extent[1]) - this.coords.x(extent[0]))
        .attr("height", this.coords.y(extent[2]) - this.coords.y(extent[3]));
};

// mpld3_Image.prototype.zoomed = function() {
//     this.updateDimensions();
// };
