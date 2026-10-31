/***********************************************************************/
/* Coordinates Object: Converts from given units to screen/pixel units */
/*   `trans` is one of ["data", "figure", "axes", "display"]           */
mpld3.Coordinates = mpld3_Coordinates;

function mpld3_Coordinates(trans, ax, fig) {
    this.trans = trans;
    this.ax = (typeof(ax) === "undefined") ? null : ax;
    this.fig = (typeof(fig) === "undefined") ? (this.ax ? this.ax.fig : null) : fig;
    if (this.ax === null && this.fig === null && this.trans !== "display")
        throw "ax or fig must be defined if transform != 'display'";
    if (this.ax === null && this.trans !== "display" && this.trans !== "figure")
        throw "ax must be defined if transform != 'display' and transform != 'figure'";
    this.zoomable = (this.trans === "data");
    this.x = this["x_" + this.trans];
    this.y = this["y_" + this.trans];
    if (typeof(this.x) === "undefined" || typeof(this.y) === "undefined")
        throw "unrecognized coordinate code: " + this.trans;
}

mpld3_Coordinates.prototype.xy = function(d, ix, iy) {
    ix = (typeof(ix) === "undefined") ? 0 : ix;
    iy = (typeof(iy) === "undefined") ? 1 : iy;
    return [this.x(d[ix]), this.y(d[iy])];
};

mpld3_Coordinates.prototype.x_data = function(x) {
    return this.ax.x(x);
}
mpld3_Coordinates.prototype.y_data = function(y) {
    return this.ax.y(y);
}
mpld3_Coordinates.prototype.x_display = function(x) {
    return x;
}
mpld3_Coordinates.prototype.y_display = function(y) {
    return y;
}
mpld3_Coordinates.prototype.x_axes = function(x) {
    return x * this.ax.width;
}
mpld3_Coordinates.prototype.y_axes = function(y) {
    return this.ax.height * (1 - y);
}
mpld3_Coordinates.prototype.x_figure = function(x) {
    return this.ax ? x * this.fig.width - this.ax.position[0] : x * this.fig.width;
}
mpld3_Coordinates.prototype.y_figure = function(y) {
    return this.ax ? (1 - y) * this.fig.height - this.ax.position[1] : (1 - y) * this.fig.height;
}
