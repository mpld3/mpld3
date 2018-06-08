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

// getBrush contains boilerplate for defining a d3 brush over the axes
mpld3_Figure.prototype.getBrush = function() {
    // TODO: (@vladh) [brush] Fix brush in figure.
    if (typeof this._brush === "undefined"){
        // use temporary linear scales here: we'll replace
        // with the real x and y scales below.
        var brush = d3.brush();

        // this connects the axes instance to the brush elements
        this.root.selectAll(".mpld3-axes")
            .data(this.axes)
            .call(brush);

        this._brush = brush;
        this.hideBrush();
    }
    return this._brush;
};

mpld3_Figure.prototype.showBrush = function(extentClass) {
    // TODO: (@vladh) [brush] Fix brush in figure.
    extentClass = (typeof extentClass === "undefined") ? "" : extentClass;
    var brush = this.getBrush();
    // TODO: (@vladh) [brush] Is this still needed?
    // brush.on("start", function(d){ brush.x(d.xdom).y(d.ydom); });
    this.canvas.selectAll("rect.overlay")
        .attr("cursor", "crosshair")
        .attr("pointer-events", null);
    this.canvas.selectAll("rect.selection, rect.handle")
        .style("display", null)
        .classed(extentClass, true);
};

mpld3_Figure.prototype.hideBrush = function(extentClass) {
    // TODO: (@vladh) [brush] Fix brush in figure.
    extentClass = (typeof extentClass === "undefined") ? "" : extentClass;
    var brush = this.getBrush();
    brush.on("start", null)
         .on("brush", null)
         .on("end", function(d){ d.axes.call(brush.move, null); });
    this.canvas.selectAll("rect.overlay")
        .attr("cursor", null)
        .attr("pointer-events", "visible");
    this.canvas.selectAll("rect.selection, rect.handle")
        .style("display", "none")
        .classed(extentClass, false);
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
    this.disable_zoom();

    for (var i = 0; i < this.plugins.length; i++) {
        this.plugins[i].draw();
    }

    this.toolbar.draw();
};

mpld3_Figure.prototype.reset = function(duration) {
    this.axes.forEach(function(ax) {
        ax.reset(duration, false);
    });
};

mpld3_Figure.prototype.enable_zoom = function() {
    console.log('[figure#enable_zoom]');
    for (var i = 0; i < this.axes.length; i++) {
        this.axes[i].enable_zoom();
    }
    this.zoom_on = true;
};

mpld3_Figure.prototype.disable_zoom = function() {
    console.log('[figure#disable_zoom]');
    for (var i = 0; i < this.axes.length; i++) {
        this.axes[i].disable_zoom();
    }
    this.zoom_on = false;
};

mpld3_Figure.prototype.toggle_zoom = function() {
    console.log('[figure#toggle_zoom] zoom_on:', this.zoom_on);
    if (this.zoom_on) {
        this.disable_zoom();
    } else {
        this.enable_zoom();
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
