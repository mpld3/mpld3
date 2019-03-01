import "../core/element";

/**********************************************************************/
/* Path Collection Element */
mpld3.PathCollection = mpld3_PathCollection;
mpld3_PathCollection.prototype =
    Object.create(mpld3_PlotElement.prototype);
mpld3_PathCollection.prototype.constructor = mpld3_PathCollection;
mpld3_PathCollection.prototype.requiredProps = ["paths", "offsets"];
mpld3_PathCollection.prototype.defaultProps = {
    xindex: 0,
    yindex: 1,
    pathtransforms: [],
    pathcoordinates: "display",
    offsetcoordinates: "data",
    offsetorder: "before",
    edgecolors: ["#000000"],
    drawstyle: "none",
    edgewidths: [1.0],
    facecolors: ["#0000FF"],
    alphas: [1.0],
    zorder: 2
};

function mpld3_PathCollection(ax, props) {
    mpld3_PlotElement.call(this, ax, props);

    if (this.props.facecolors == null ||
        this.props.facecolors.length == 0) {
        this.props.facecolors = ["none"];
    }
    if (this.props.edgecolors == null ||
        this.props.edgecolors.length == 0) {
        this.props.edgecolors = ["none"];
    }

    var offsets = this.ax.fig.get_data(this.props.offsets);
    if (offsets === null || offsets.length === 0)
        offsets = [null];

    // For use in the draw() command, expand offsets to size N
    var N = Math.max(this.props.paths.length, offsets.length);
    if (offsets.length === N) {
        this.offsets = offsets;
    } else {
        this.offsets = [];
        for (var i = 0; i < N; i++)
            this.offsets.push(getMod(offsets, i));
    }

    this.pathcoords =
        new mpld3_Coordinates(this.props.pathcoordinates, this.ax);
    this.offsetcoords =
        new mpld3_Coordinates(this.props.offsetcoordinates, this.ax);
}

mpld3_PathCollection.prototype.transformFunc = function(d, i) {
    var t = this.props.pathtransforms;
    var transform = (t.length == 0) ? "" :
        mpld3.getTransformation("matrix(" + getMod(t, i) + ")").toString();

    var offset = (d === null || typeof(d) === "undefined") ?
        "translate(0, 0)" :
        ("translate(" + this.offsetcoords.xy(d, this.props.xindex,
        this.props.yindex) + ")");

    return (this.props.offsetorder === "after") ? transform + offset : offset + transform;
};

mpld3_PathCollection.prototype.pathFunc = function(d, i) {
    return mpld3_path()
        .x(function(d) {
            return this.pathcoords.x(d[0]);
        }.bind(this))
        .y(function(d) {
            return this.pathcoords.y(d[1]);
        }.bind(this))
        .apply(this, getMod(this.props.paths, i));
};

mpld3_PathCollection.prototype.styleFunc = function(d, i) {
    var styles = {
        "stroke": getMod(this.props.edgecolors, i),
        "stroke-width": getMod(this.props.edgewidths, i),
        "stroke-opacity": getMod(this.props.alphas, i),
        "fill": getMod(this.props.facecolors, i),
        "fill-opacity": getMod(this.props.alphas, i),
    }
    var ret = ""
    for (var key in styles) {
        ret += key + ":" + styles[key] + ";"
    }
    return ret
};

mpld3_PathCollection.prototype.allFinite = function(d) {
    if (d instanceof Array) {
        return (d.length == d.filter(isFinite).length);
    } else {
        return true;
    }
}

mpld3_PathCollection.prototype.draw = function() {
    // TODO: (@vladh) Don't fully understand this.
    if (this.offsetcoords.zoomable || this.pathcoords.zoomable) {
        this.group = this.ax.paths.append("svg:g");
    } else {
        this.group = this.ax.staticPaths.append("svg:g");
    }

    this.pathsobj = this.group.selectAll("paths")
        .data(this.offsets.filter(this.allFinite))
        .enter().append("svg:path")
        .attr("d", this.pathFunc.bind(this))
        .attr("class", "mpld3-path")
        .attr("transform", this.transformFunc.bind(this))
        .attr("style", this.styleFunc.bind(this))
        .attr("vector-effect", "non-scaling-stroke");
};

mpld3_PathCollection.prototype.elements = function(d) {
    return this.group.selectAll("path");
};

// TODO: (@vladh) Remove legacy zooming code.
// mpld3_PathCollection.prototype.zoomed = function() {
//     if (this.props.pathcoordinates === "data") {
//         this.pathsobj.attr("d", this.pathFunc.bind(this));
//     }
//     if (this.props.offsetcoordinates === "data") {
//         this.pathsobj.attr("transform", this.transformFunc.bind(this));
//     }
// };
