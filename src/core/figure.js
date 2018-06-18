import "element";
import "axes";
import "../toolbar/";
import "../plugins/";

/**********************************************************************/
/* Figure object: */
mpld3.Figure = mpld3_Figure;
mpld3_Figure.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Figure.prototype.constructor = mpld3_Figure;
mpld3_Figure.prototype.requiredProps = ["width", "height"];
mpld3_Figure.prototype.defaultProps = {
    data: {},
    axes: [],
    plugins: [{type: "reset"}, {type: "zoom"}, {type: "boxzoom"}]
};

function mpld3_Figure(figid, props) {
    mpld3_PlotElement.call(this, null, props);
    this.figid = figid;
    this.width = this.props.width;
    this.height = this.props.height;
    this.data = this.props.data;
    this.buttons = [];

    // Make a root div with relative positioning,
    // so we can position elements absolutely within it.
    this.root = d3.select('#' + figid)
        .append("div").style("position", "relative");

    this.isZoomEnabled = null
    this.zoom = d3.zoom();

    // Create all the axes elements in the figure
    this.axes = [];
    for (var i = 0; i < this.props.axes.length; i++)
        this.axes.push(new mpld3_Axes(this, this.props.axes[i]));

    // Connect the plugins to the figure
    this.plugins = [];
    this.props.plugins.forEach(function(plugin) {
        this.addPlugin(plugin);
    }.bind(this));

    // Create the figure toolbar. Do this last because plugins may modify the
    // button list.
    // TODO: (@vladh) Refactor this to fix tight coupling and mutation.
    this.toolbar = new mpld3.Toolbar(this, {
        buttons: this.buttons
    });
}

mpld3_Figure.prototype.zoomed = function() {
    if (!this.isZoomEnabled) {
        return;
    }
    this.axes.forEach(function(axes) {
        axes.zoomed(null, d3.event.transform);
    }.bind(this));
}

mpld3_Figure.prototype.getBrush = function() {
    return undefined;
};

mpld3_Figure.prototype.addPlugin = function(pluginInfo) {
    if (!pluginInfo.type) {
        return console.warn("unspecified plugin type. Skipping this");
    }

    var plugin;
    if (pluginInfo.type in mpld3.plugin_map) {
        plugin = mpld3.plugin_map[pluginInfo.type];
    } else {
        return console.warn("Skipping unrecognized plugin: " + plugin);
    }

    if (pluginInfo.clear_toolbar || pluginInfo.buttons) {
        console.warn(
            'DEPRECATION WARNING: ' +
            'You are using pluginInfo.clear_toolbar or pluginInfo, which ' +
            'have been deprecated. Please see the build-in plugins for the new ' +
            'method to add buttons, otherwise contact the mpld3 maintainers.'
        );
    }

    // Not sure why we need to take the type out.
    var pluginInfoNoType = mpld3_cloneObj(pluginInfo);
    delete pluginInfoNoType.type;

    this.plugins.push(new plugin(this, pluginInfoNoType));
};

mpld3_Figure.prototype.draw = function() {
    this.canvas = this.root.append('svg:svg')
        .attr('class', 'mpld3-figure')
        .attr('width', this.width)
        .attr('height', this.height);

    for (var i = 0; i < this.axes.length; i++) {
        this.axes[i].draw();
    }

    // disable zoom by default; plugins or toolbar items might change this.
    this.disableZoom();

    for (var i = 0; i < this.plugins.length; i++) {
        this.plugins[i].draw();
    }

    this.toolbar.draw();
};

mpld3_Figure.prototype.reset = function(duration) {
    // TODO: (@vladh) Multiple axes.
    this.axes[0].axes.transition()
        .duration(750)
        .call(this.zoom.transform, d3.zoomIdentity);
};

mpld3_Figure.prototype.enableZoom = function() {
    this.isZoomEnabled = true;
    this.zoom.on('zoom', this.zoomed.bind(this));
    // TODO: (@vladh) Multiple axes.
    this.axes[0].axes.call(this.zoom);
    this.axes[0].axes.style('cursor', 'move');
};

mpld3_Figure.prototype.disableZoom = function() {
    this.isZoomEnabled = false;
    this.zoom.on('zoom', null);
    // TODO: (@vladh) Multiple axes.
    this.axes[0].axes.on('.zoom', null);
    this.axes[0].axes.style('cursor', null);
};

mpld3_Figure.prototype.toggleZoom = function() {
    if (this.isZoomEnabled) {
        this.disableZoom();
    } else {
        this.enableZoom();
    }
};

mpld3_Figure.prototype.get_data = function(data) {
    if (data === null || typeof(data) === "undefined") {
        return null;
    } else if (typeof(data) === "string") {
        return this.data[data];
    } else {
        return data;
    }
}
