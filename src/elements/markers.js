import "path_collection"

/**********************************************************************/
/* Markers Element */
mpld3.Markers = mpld3_Markers;
mpld3_Markers.prototype = Object.create(mpld3_PathCollection.prototype);
mpld3_Markers.prototype.constructor = mpld3_Markers;
mpld3_Markers.prototype.requiredProps = ["data"];
mpld3_Markers.prototype.defaultProps = {
    xindex: 0,
    yindex: 1,
    coordinates: "data",
    facecolor: "salmon",
    edgecolor: "black",
    edgewidth: 1,
    alpha: 1.0,
    markersize: 6,
    markername: "circle",
    drawstyle: "none",
    markerpath: null,
    zorder: 3
};

function mpld3_Markers(ax, props) {
    mpld3_PlotElement.call(this, ax, props);

    // Construct the marker path
    if (this.props.markerpath !== null) {
        this.marker = (this.props.markerpath[0].length == 0) ? null :
            mpld3.path().call(this.props.markerpath[0],
                this.props.markerpath[1]);
    } else {
        this.marker = (this.props.markername === null) ? null :
            d3.symbol(this.props.markername)
              .size(Math.pow(this.props.markersize, 2))();
    }

    //
    // Call the PathCollection constructor
    var PCprops = {
        paths: [this.props.markerpath],
        offsets: ax.fig.parse_offsets(ax.fig.get_data(this.props.data, true)),
        xindex: this.props.xindex,
        yindex: this.props.yindex,
        offsetcoordinates: this.props.coordinates,
        edgecolors: [this.props.edgecolor],
        edgewidths: [this.props.edgewidth],
        facecolors: [this.props.facecolor],
        alphas: [this.props.alpha],
        zorder: this.props.zorder,
        id: this.props.id
    }
    this.requiredProps = mpld3_PathCollection.prototype.requiredProps;
    this.defaultProps = mpld3_PathCollection.prototype.defaultProps;
    mpld3_PathCollection.call(this, ax, PCprops);
};

mpld3_Markers.prototype.pathFunc = function(d, i) {
    return this.marker;
};
