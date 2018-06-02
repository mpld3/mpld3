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
    console.log('[axes#draw]');
    for (var i = 0; i < this.props.sharex.length; i++) {
        this.sharex.push(mpld3.get_element(this.props.sharex[i]));
    }

    for (var i = 0; i < this.props.sharey.length; i++) {
        this.sharey.push(mpld3.get_element(this.props.sharey[i]));
    }

    this.zoom = d3.zoom();

    // TODO: (@vladh) [zoom] Fix secondary zoom stuff.
    // this.zoom.last_t = this.zoom.translate()
    // this.zoom.last_s = this.zoom.scale()
    // this.zoom_x = d3.zoom().x(this.xdom);
    // this.zoom_y = d3.zoom().y(this.ydom);

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

    for (var i = 0; i < this.elements.length; i++) {
        this.elements[i].draw();
    }

    // TODO: (@vladh) [zoom] This wasn't needed before, why is it now?
    // this.enable_zoom();
};

// TODO: (@vladh) [zoom] Fix zoom on axis.
mpld3_Axes.prototype.enable_zoom = function() {
    console.log('[axes#enable_zoom]');
    if (this.props.zoomable) {
        this.zoom.on("zoom", this.zoomed.bind(this, true));
        // TODO: (@vladh) [zoom] Fix this.
        this.axes.call(this.zoom);
        this.axes.style("cursor", 'move');
    }
};

mpld3_Axes.prototype.disable_zoom = function() {
    console.log('[axes#disable_zoom]');
    if (this.props.zoomable) {
        this.zoom.on("zoom", null);
        // TODO: (@vladh) [zoom] Fix this.
        this.axes.on('.zoom', null)
        this.axes.style('cursor', null);
    }
};

mpld3_Axes.prototype.zoomed = function(propagate) {
    console.log('[axes#zoomed]');
    // TODO: (@vladh) [zoom] Fix zoom propagation.
    // // propagate is a boolean specifying whether to propagate movements
    // // to shared axes, specified by sharex and sharey.  Default is true.
    // propagate = (typeof propagate == 'undefined') ? true : propagate;
    // if (propagate) {
    //     // update scale and translation of zoom_x and zoom_y,
    //     // based on change in this.zoom scale and translation values
    //     var dt0 = this.zoom.translate()[0] - this.zoom.last_t[0];
    //     var dt1 = this.zoom.translate()[1] - this.zoom.last_t[1];
    //     var ds = this.zoom.scale() / this.zoom.last_s;

    //     this.zoom_x.translate([this.zoom_x.translate()[0] + dt0, 0]);
    //     this.zoom_x.scale(this.zoom_x.scale() * ds)

    //     this.zoom_y.translate([0, this.zoom_y.translate()[1] + dt1]);
    //     this.zoom_y.scale(this.zoom_y.scale() * ds)

    //     // update last translate and scale values for future use
    //     this.zoom.last_t = this.zoom.translate();
    //     this.zoom.last_s = this.zoom.scale();

    //     // update shared axes objects
    //     this.sharex.forEach(function(ax) {
    //         ax.zoom_x.translate(this.zoom_x.translate())
    //             .scale(this.zoom_x.scale());
    //     }.bind(this));
    //     this.sharey.forEach(function(ax) {
    //         ax.zoom_y.translate(this.zoom_y.translate())
    //             .scale(this.zoom_y.scale());
    //     }.bind(this));

    //     // render updates
    //     this.sharex.forEach(function(ax) {
    //         ax.zoomed(false);
    //     });
    //     this.sharey.forEach(function(ax) {
    //         ax.zoomed(false);
    //     });
    // }

    // for (var i = 0; i < this.elements.length; i++) {
    //     this.elements[i].zoomed();
    // }
};

mpld3_Axes.prototype.reset = function(duration, propagate) {
    this.set_axlim(
        this.props.xdomain, this.props.ydomain, duration, propagate
    );
};

mpld3_Axes.prototype.set_axlim = function(
    xlim, ylim, duration, propagate, bounds
) {
    console.log('[axes#set_axlim]');
    console.log(bounds);
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

    // TODO: (@vladh) [zoom] Fix zoom transition.
    /*
    var transition = function(t) {
        this.zoom_x.x(this.xdom.domain(interpX(t)));
        this.zoom_y.y(this.ydom.domain(interpY(t)));
        this.zoomed(false); // don't propagate here; propagate below.
    }.bind(this);
    */

    // select({}) is a trick to make transitions run concurrently
    // d3.select({})
    //     .transition().duration(duration)
    //     .tween("zoom", function() {
    //         return transition;
    //     });
    if (!bounds) {
        console.error('[axes#set_axlim] Tried to zoom, but got no bounds.');
        return;
    }
    transform = mpld3.boundsToTransform(this.fig, bounds);
    console.log('DO IT');
    this.axes.call(this.zoom.transform, d3.zoomIdentity.translate(100, 100).scale(0.5));
    // this.fig.canvas
    //     .transition()
    //     .duration(750)
    //     .call(
    //         this.zoom.transform,
    //         d3.zoomIdentity
    //             .translate(transform.translate[0], transform.translate[1])
    //             .scale(transform.scale)
    //     );

    // TODO: (@vladh) [zoom] Fix zoom propagation.
    // propagate axis limits to shared axes
    // if (propagate) {
    //     this.sharex.forEach(function(ax) {
    //         ax.set_axlim(xlim, null, duration, false);
    //     });
    //     this.sharey.forEach(function(ax) {
    //         ax.set_axlim(null, ylim, duration, false);
    //     });
    // }

    // TODO: (@vladh) [zoom] Fix other zoom that might not be needed.
    // finalize the reset operation.
    // this.zoom.last_t = this.zoom.translate();
    // this.zoom.last_s = this.zoom.scale();
    // this.zoom_x.scale(1).translate([0, 0]);
    // this.zoom_y.scale(1).translate([0, 0]);
};
