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

    var bbox = this.props.bbox;
    this.position = [bbox[0] * this.fig.width, (1 - bbox[1] - bbox[3]) * this.fig.height];
    this.width = bbox[2] * this.fig.width;
    this.height = bbox[3] * this.fig.height;

    this.isZoomEnabled = null;
    this.zoom = d3.zoom();
    this.lastTransform = d3.zoomIdentity;

    this.isBoxzoomEnabled = null;

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

    this.clip = this.baseaxes.append("svg:clipPath")
        .attr("id", this.clipid)
        .append("svg:rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", this.width)
        .attr("height", this.height)

    this.axes = this.baseaxes.append("g")
        .attr("class", "mpld3-axes")
        .attr("clip-path", "url(#" + this.clipid + ")");

    this.axesbg = this.axes.append("svg:rect")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("class", "mpld3-axesbg")
        .style("fill", this.props.axesbg)
        .style("fill-opacity", this.props.axesbgalpha);

    this.paths = this.axes.append("g")
        .attr("class", "mpld3-paths");

    this.brush = d3.brush().extent([
        [0, 0], [this.fig.width, this.fig.height],
    ])
        .on('start', this.brushStart.bind(this))
        .on('brush', this.brushBrush.bind(this))
        .on('end', this.brushEnd.bind(this))
        .on('start.nokey', function() {
            d3.select(window).on('keydown.brush keyup.brush', null);
        });

    this.brushG = null;

    // We use this.zoom both for zoom and boxzoom, and potentially for other
    // things too, so we'll just enable it here and leave it enabled.
    this.bindZoom();

    for (var i = 0; i < this.elements.length; i++) {
        this.elements[i].draw();
    }
};

mpld3_Axes.prototype.bindZoom = function() {
    this.zoom.on('zoom', this.zoomed.bind(this));
    this.axes.call(this.zoom);
    this.axes.style('cursor', 'move');
};

mpld3_Axes.prototype.unbindZoom = function() {
    this.zoom.on('zoom', null);
    this.axes.on('.zoom', null);
    this.axes.style('cursor', null);
};

mpld3_Axes.prototype.reset = function() {
    this.doZoom(false, d3.zoomIdentity, 750);
};

mpld3_Axes.prototype.enableBoxzoom = function() {
    this.isBoxzoomEnabled = true;
    this.brushG = this.axes
        .append('g')
        .attr('class', 'brush')
        .call(this.brush);
};

mpld3_Axes.prototype.disableBoxzoom = function() {
    this.isBoxzoomEnabled = false;
    if (this.brushG) {
        this.brushG.remove();
        this.brushG.on('.brush', null);
    }
};

mpld3_Axes.prototype.enableZoom = function() {
    this.isZoomEnabled = true;
};

mpld3_Axes.prototype.disableZoom = function() {
    this.isZoomEnabled = false;
};

mpld3_Axes.prototype.doZoom = function(propagate, transform, duration) {
    if (!(this.props.zoomable && (this.isZoomEnabled || this.isBoxzoomEnabled))) {
        return;
    }

    // console.log(propagate, transform, this.lastTransform, kDiff);

    if (duration) {
        this.axes
            .transition()
            .duration(duration)
            .call(this.zoom.transform, transform);
    } else {
        this.axes
            .call(this.zoom.transform, transform);
    }

    if (propagate) {
        var xDiff = transform.x - this.lastTransform.x;
        var yDiff = transform.y - this.lastTransform.y;
        var kDiff = 1 + transform.k - this.lastTransform.k;

        this.lastTransform = transform;

        this.sharex.forEach(function(sharedAxes) {
            var xTransform = sharedAxes.lastTransform.translate(xDiff, 0).scale(kDiff);
            sharedAxes.doZoom(false, xTransform, duration);
        });

        this.sharey.forEach(function(sharedAxes) {
            var yTransform = sharedAxes.lastTransform.translate(0, yDiff).scale(kDiff);
            sharedAxes.doZoom(false, yTransform, duration);
        });
    } else {
        this.lastTransform = transform;
    }
};

mpld3_Axes.prototype.zoomed = function() {
    // If called from an event (i.e. actual mouse movement).
    if (d3.event.sourceEvent && d3.event.sourceEvent.constructor.name != 'ZoomEvent') {
        this.doZoom(true, d3.event.transform, false);
    // If called programmatically.
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

mpld3_Axes.prototype.brushStart = function() {
};

// Sorry for this function name.
mpld3_Axes.prototype.brushBrush = function() {
};

mpld3_Axes.prototype.brushEnd = function() {
    if (!d3.event.selection || !this.fig.canvas || !this.brushG) {
        return;
    }

    var bounds = d3.event.selection;
    var axesDimensions = this.axesbg.node().getBBox();
    var width = axesDimensions.width;
    var height = axesDimensions.height;

    var dx = bounds[1][0] - bounds[0][0];
    var dy = bounds[1][1] - bounds[0][1];
    var cx = (bounds[0][0] + bounds[1][0]) / 2;
    var cy = (bounds[0][1] + bounds[1][1]) / 2;
    var scale = Math.max(1, Math.min(8, 0.85 / Math.max(dx / width, dy / height)));
    var translate = [width / 2 - scale * cx, height / 2 - scale * cy];

    this.brushG.call(this.brush.move, null);

    var transform = d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale);
    this.doZoom(true, transform, 750);
};

// TODO: (@vladh) Remove this when no longer needed.
/*
mpld3_Axes.prototype.reset = function(duration, propagate) {
    this.set_axlim(
        this.props.xdomain, this.props.ydomain, duration, propagate
    );
};

mpld3_Axes.prototype.set_axlim = function(
    xlim, ylim, duration, propagate, bounds
) {
    // => zoom set_axlim?

    // xlim = isUndefinedOrNull(xlim) ? this.xdom.domain() : xlim;
    // ylim = isUndefinedOrNull(ylim) ? this.ydom.domain() : ylim;
    // duration = isUndefinedOrNull(duration) ? 750 : duration;
    // propagate = isUndefined(propagate) ? true : propagate;

    // // Create a transition function which will interpolate
    // // from the current axes limits to the final limits
    // var interpX = (this.props.xscale === 'date') ?
    //     mpld3.interpolateDates(this.xdom.domain(), xlim) :
    //     d3.interpolate(this.xdom.domain(), xlim);

    // var interpY = (this.props.yscale === 'date') ?
    //     mpld3.interpolateDates(this.ydom.domain(), ylim) :
    //     d3.interpolate(this.ydom.domain(), ylim);

    // if (!bounds) {
    //     console.error('[axes#set_axlim] Tried to zoom, but got no bounds.');
    //     return;
    // }
    // transform = mpld3.boundsToTransform(this.fig, bounds);
    // this.axes.call(this.zoom.transform, d3.zoomIdentity.translate(100, 100).scale(0.5));

    // var transition = function(t) {
    //     this.zoom_x.x(this.xdom.domain(interpX(t)));
    //     this.zoom_y.y(this.ydom.domain(interpY(t)));
    //     this.zoomed(false); // don't propagate here; propagate below.
    // }.bind(this);

    // select({}) is a trick to make transitions run concurrently
    // d3.select({})
    //     .transition().duration(duration)
    //     .tween("zoom", function() {
    //         return transition;
    //     });

    // propagate axis limits to shared axes
    // if (propagate) {
    //     this.sharex.forEach(function(ax) {
    //         ax.set_axlim(xlim, null, duration, false);
    //     });
    //     this.sharey.forEach(function(ax) {
    //         ax.set_axlim(null, ylim, duration, false);
    //     });
    // }

    // finalize the reset operation.
    // this.zoom.last_t = this.zoom.translate();
    // this.zoom.last_s = this.zoom.scale();
    // this.zoom_x.scale(1).translate([0, 0]);
    // this.zoom_y.scale(1).translate([0, 0]);
};
*/
