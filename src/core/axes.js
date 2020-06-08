import "element";
import "axis";
import "../elements/";
import "../utils/";

/**********************************************************************/
/* Axes Object: */
mpld3.Axes = mpld3_Axes;
mpld3_Axes.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Axes.prototype.constructor = mpld3_Axes;
mpld3_Axes.prototype.requiredProps = ["xlim", "ylim"];
mpld3_Axes.prototype.defaultProps = {
    "bbox": [0.1, 0.1, 0.8, 0.8],
    "axesbg": "#FFFFFF",
    "axesbgalpha": 1.0,
    "gridOn": false,
    "xdomain": null,
    "ydomain": null,
    "xscale": "linear",
    "yscale": "linear",
    "zoomable": true,
    "axes": [{
        position: "left"
    }, {
        position: "bottom"
    }],
    "lines": [],
    "paths": [],
    "markers": [],
    "texts": [],
    "collections": [],
    "sharex": [],
    "sharey": [],
    "images": []
};

function mpld3_Axes(fig, props) {
    mpld3_PlotElement.call(this, fig, props);
    this.axnum = this.fig.axes.length;
    this.axid = this.fig.figid + '_ax' + (this.axnum + 1)
    this.clipid = this.axid + '_clip'
    this.props.xdomain = this.props.xdomain || this.props.xlim;
    this.props.ydomain = this.props.ydomain || this.props.ylim;

    this.sharex = [];
    this.sharey = [];

    this.elements = [];
    this.axisList = []; // Badly named, to avoid conflicts.

    var bbox = this.props.bbox;
    this.position = [bbox[0] * this.fig.width, (1 - bbox[1] - bbox[3]) * this.fig.height];
    this.width = bbox[2] * this.fig.width;
    this.height = bbox[3] * this.fig.height;

    this.isZoomEnabled = null;
    this.zoom = null;
    this.lastTransform = d3.zoomIdentity;

    this.isBoxzoomEnabled = null;

    this.isLinkedBrushEnabled = null;
    this.isCurrentLinkedBrushTarget = false;
    this.brushG = null;

    // In the case of date scales, set the domain

    function buildDate(d) {
        return new Date(d[0], d[1], d[2], d[3], d[4], d[5]);
    }

    function setDomain(scale, domain) {
        return (scale !== "date") ? domain : [buildDate(domain[0]),
            buildDate(domain[1])
        ];
    }

    this.props.xdomain = setDomain(this.props.xscale, this.props.xdomain);
    this.props.ydomain = setDomain(this.props.yscale, this.props.ydomain);

    /*****************************************************************
    There are 3 different scales which come into play with axes.
           - screen pixel scale
           - data range
           - data domain
    The data range and domain are only different in the case of
    date axes.  For log or linear axes, the two are identical.

    To convert between these, we have the following mappings:
     - [x,y]dom     : map from domain to screen
     - [x,y]        : map from range to screen
    Here we'll construct these mappings.
  *****************************************************************/

    function build_scale(scale, domain, range) {
        var dom = (scale === 'date') ? d3.scaleTime() :
            (scale === 'log') ? d3.scaleLog() : d3.scaleLinear();
        return dom.domain(domain).range(range);
    }

    this.x = this.xdom = build_scale(this.props.xscale,
        this.props.xdomain, [0, this.width]);

    this.y = this.ydom = build_scale(this.props.yscale,
        this.props.ydomain, [this.height, 0]);

    if (this.props.xscale === "date") {
        this.x = mpld3.multiscale(d3.scaleLinear()
                                    .domain(this.props.xlim)
                                    .range(this.props.xdomain.map(Number)),
                                  this.xdom);
    }

    if (this.props.yscale === "date") {
        this.y = mpld3.multiscale(d3.scaleLinear()
                                    .domain(this.props.ylim)
                                    .range(this.props.ydomain.map(Number)),
                                  this.ydom);
    }

    // Add axes and grids
    var axes = this.props.axes;
    for (var i = 0; i < axes.length; i++) {
        var axis = new mpld3.Axis(this, axes[i])
        this.axisList.push(axis);
        this.elements.push(axis);
        if (this.props.gridOn || axis.props.grid.gridOn) {
            this.elements.push(axis.getGrid());
        }
    }

    // Add paths
    var paths = this.props.paths;
    for (var i = 0; i < paths.length; i++) {
        this.elements.push(new mpld3.Path(this, paths[i]));
    }

    // Add lines
    var lines = this.props.lines;
    for (var i = 0; i < lines.length; i++) {
        this.elements.push(new mpld3.Line(this, lines[i]));
    }

    // Add markers
    var markers = this.props.markers;
    for (var i = 0; i < markers.length; i++) {
        this.elements.push(new mpld3.Markers(this, markers[i]));
    }

    // Add texts
    var texts = this.props.texts;
    for (var i = 0; i < texts.length; i++) {
        this.elements.push(new mpld3.Text(this, texts[i]));
    }

    // Add collections
    var collections = this.props.collections;
    for (var i = 0; i < collections.length; i++) {
        this.elements.push(new mpld3.PathCollection(this, collections[i]));
    }

    // Add images
    var images = this.props.images;
    for (var i = 0; i < images.length; i++) {
        this.elements.push(new mpld3.Image(this, images[i]));
    }

    // Sort all elements by zorder
    this.elements.sort(function(a, b) {
        return a.props.zorder - b.props.zorder
    });
}

mpld3_Axes.prototype.draw = function() {
    for (var i = 0; i < this.props.sharex.length; i++) {
        this.sharex.push(mpld3.get_element(this.props.sharex[i]));
    }
    for (var i = 0; i < this.props.sharey.length; i++) {
        this.sharey.push(mpld3.get_element(this.props.sharey[i]));
    }

    this.baseaxes = this.fig.canvas.append("g")
        .attr('transform', 'translate(' + this.position[0] + ',' + this.position[1] + ')')
        .attr('width', this.width)
        .attr('height', this.height)
        .attr('class', "mpld3-baseaxes");

    this.axes = this.baseaxes.append("g")
        .attr("class", "mpld3-axes")
        .style("pointer-events", "visiblefill");

    this.clip = this.axes.append("svg:clipPath")
        .attr("id", this.clipid)
        .append("svg:rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", this.width)
        .attr("height", this.height)

    this.axesbg = this.axes.append("svg:rect")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("class", "mpld3-axesbg")
        .style("fill", this.props.axesbg)
        .style("fill-opacity", this.props.axesbgalpha);

    this.pathsContainer = this.axes.append("g")
        .attr("clip-path", "url(#" + this.clipid + ")")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("class", "mpld3-paths-container");

    this.paths = this.pathsContainer.append("g")
        .attr("class", "mpld3-paths");

    this.staticPaths = this.axes.append("g")
        .attr("class", "mpld3-staticpaths");

    this.brush = d3.brush().extent([
        [0, 0], [this.fig.width, this.fig.height],
    ])
        .on('start', this.brushStart.bind(this))
        .on('brush', this.brushMove.bind(this))
        .on('end', this.brushEnd.bind(this))
        .on('start.nokey', function() {
            d3.select(window).on('keydown.brush keyup.brush', null);
        });

    for (var i = 0; i < this.elements.length; i++) {
        this.elements[i].draw();
    }
};

mpld3_Axes.prototype.bindZoom = function() {
    if (!this.zoom) {
        this.zoom = d3.zoom();
        this.zoom.on('zoom', this.zoomed.bind(this));
        this.axes.call(this.zoom);
    }
};

mpld3_Axes.prototype.unbindZoom = function() {
    if (this.zoom) {
        this.zoom.on('zoom', null);
        this.axes.on('.zoom', null);
        this.zoom = null;
    }
};

mpld3_Axes.prototype.bindBrush = function() {
    if (!this.brushG) {
        this.brushG = this.axes
            .append('g')
            .attr('class', 'mpld3-brush')
            .call(this.brush);
    }
};

mpld3_Axes.prototype.unbindBrush = function() {
    if (this.brushG) {
        this.brushG.remove();
        this.brushG.on('.brush', null);
        this.brushG = null;
    }
};

mpld3_Axes.prototype.reset = function() {
    if (this.zoom) {
        this.doZoom(false, d3.zoomIdentity, 750);
    } else {
        this.bindZoom();
        this.doZoom(false, d3.zoomIdentity, 750, function() {
            /*
            (@vladh)

            If zoom was not bound before, but we now have some type
            of zoom enabled, what probably happened is that the user enabled
            zoom/boxzoom during this transition, in which case we don't want
            to disable zoom anymore.

            BUG: If the user does this, there will be a weird break in the
            animation until they zoom again. This is because of the toolbar
            behaviour and can't be fixed here. We should fix it in the future
            though.
            */
            if (this.isSomeTypeOfZoomEnabled) {
                return;
            }
            this.unbindZoom();
        }.bind(this));
    }
};

mpld3_Axes.prototype.enableOrDisableBrushing = function() {
    if (this.isBoxzoomEnabled || this.isLinkedBrushEnabled) {
        this.bindBrush();
    } else {
        this.unbindBrush();
    }
};

mpld3_Axes.prototype.isSomeTypeOfZoomEnabled = function() {
    return this.isZoomEnabled || this.isBoxzoomEnabled;
};

mpld3_Axes.prototype.enableOrDisableZooming = function() {
    if (this.isSomeTypeOfZoomEnabled()) {
        this.bindZoom();
    } else {
        this.unbindZoom();
    }
};

mpld3_Axes.prototype.enableLinkedBrush = function() {
    this.isLinkedBrushEnabled = true;
    this.enableOrDisableBrushing();
};

mpld3_Axes.prototype.disableLinkedBrush = function() {
    this.isLinkedBrushEnabled = false;
    this.enableOrDisableBrushing();
};

mpld3_Axes.prototype.enableBoxzoom = function() {
    this.isBoxzoomEnabled = true;
    this.enableOrDisableBrushing();
    this.enableOrDisableZooming();
};

mpld3_Axes.prototype.disableBoxzoom = function() {
    this.isBoxzoomEnabled = false;
    this.enableOrDisableBrushing();
    this.enableOrDisableZooming();
};

mpld3_Axes.prototype.enableZoom = function() {
    this.isZoomEnabled = true;
    this.enableOrDisableZooming();
    this.axes.style('cursor', 'move');
};

mpld3_Axes.prototype.disableZoom = function() {
    this.isZoomEnabled = false;
    this.enableOrDisableZooming();
    this.axes.style('cursor', null);
};

mpld3_Axes.prototype.doZoom = function(
    propagate, transform, duration, onTransitionEnd
) {
    if (!this.props.zoomable || !this.zoom) {
        return;
    }

    if (duration) {
        var transition = this.axes
            .transition()
            .duration(duration)
            .call(this.zoom.transform, transform);
        if (onTransitionEnd) {
            transition.on('end', onTransitionEnd);
        }
    } else {
        this.axes
            .call(this.zoom.transform, transform);
    }

    if (propagate) {
        // var xDiff = transform.x - this.lastTransform.x;
        // var yDiff = transform.y - this.lastTransform.y;
        // var kDiffFactor = transform.k / this.lastTransform.k;
        this.lastTransform = transform;

        this.sharex.forEach(function(sharedAxes) {
            sharedAxes.doZoom(false, transform, duration);
            // var xTransform = sharedAxes.lastTransform.translate(xDiff, 0).scale(kDiffFactor);
            // sharedAxes.doZoom(false, xTransform, duration);
        });

        this.sharey.forEach(function(sharedAxes) {
            sharedAxes.doZoom(false, transform, duration);
            // var yTransform = sharedAxes.lastTransform.translate(0, yDiff).scale(kDiffFactor);
            // sharedAxes.doZoom(false, yTransform, duration);
        });
    } else {
        this.lastTransform = transform;
    }
};

mpld3_Axes.prototype.zoomed = function() {
    var isProgrammatic =
        (d3.event.sourceEvent && d3.event.sourceEvent.type != 'zoom');

    if (isProgrammatic) {
        this.doZoom(true, d3.event.transform, false);
    } else {
        var transform = d3.event.transform;
        this.paths.attr('transform', transform);
        this.elements.forEach(function(element) {
            if (element.zoomed) {
                element.zoomed(transform);
            }
        }.bind(this));
    }
};

mpld3_Axes.prototype.resetBrush = function() {
    this.brushG.call(this.brush.move, null);
};

mpld3_Axes.prototype.doBoxzoom = function(selection) {
    if (!selection || !this.brushG) {
        return;
    }

    var sel = selection.map(this.lastTransform.invert, this.lastTransform);

    var dx = sel[1][0] - sel[0][0];
    var dy = sel[1][1] - sel[0][1];
    var cx = (sel[0][0] + sel[1][0]) / 2;
    var cy = (sel[0][1] + sel[1][1]) / 2;

    var scale = (dx > dy) ? this.width / dx : this.height / dy;
    var transX = this.width / 2 - scale * cx;
    var transY = this.height / 2 - scale * cy;
    var transform = d3.zoomIdentity.translate(transX, transY).scale(scale);

    this.doZoom(true, transform, 750);
    this.resetBrush();
}

mpld3_Axes.prototype.brushStart = function() {
    if (this.isLinkedBrushEnabled) {
        this.isCurrentLinkedBrushTarget =
            (d3.event.sourceEvent.constructor.name == 'MouseEvent');
        if (this.isCurrentLinkedBrushTarget) {
            this.fig.resetBrushForOtherAxes(this.axid);
        }
    }
};

mpld3_Axes.prototype.brushMove = function() {
    var selection = d3.event.selection;
    if (this.isLinkedBrushEnabled) {
        this.fig.updateLinkedBrush(selection);
    }
};

mpld3_Axes.prototype.brushEnd = function() {
    var selection = d3.event.selection;
    if (this.isBoxzoomEnabled) {
        this.doBoxzoom(selection);
    }
    if (this.isLinkedBrushEnabled) {
        if (!selection) {
            this.fig.endLinkedBrush();
        }
        this.isCurrentLinkedBrushTarget = false;
    }
};

mpld3_Axes.prototype.setTicks = function(xy, nr, format) {
    this.axisList.forEach(function(axis) {
        if (axis.props.xy == xy) {
            axis.setTicks(nr, format);
        }
    });
};
