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
    this.pluginsByType = {};
    this.props.plugins.forEach(function(plugin) {
        this.addPlugin(plugin);
    }.bind(this));

    // Create the figure toolbar. Do this last because plugins may modify the
    // button list.
    this.toolbar = new mpld3.Toolbar(this, {
        buttons: this.buttons
    });
}

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

    var pluginInstance = new plugin(this, pluginInfoNoType);
    this.plugins.push(pluginInstance);
    this.pluginsByType[pluginInfo.type] = pluginInstance;
};

mpld3_Figure.prototype.draw = function() {
    mpld3.insert_css('div#' + this.figid, {
        'font-family': 'Helvetica, sans-serif',
    });

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

mpld3_Figure.prototype.resetBrushForOtherAxes = function(currentAxid) {
    this.axes.forEach(function(axes) {
        if (axes.axid != currentAxid) {
            axes.resetBrush();
        }
    });
};

mpld3_Figure.prototype.updateLinkedBrush = function(selection) {
    if (!this.pluginsByType.linkedbrush) {
        return;
    }
    this.pluginsByType.linkedbrush.update(selection);
};

mpld3_Figure.prototype.endLinkedBrush = function() {
    if (!this.pluginsByType.linkedbrush) {
        return;
    }
    this.pluginsByType.linkedbrush.end();
};

mpld3_Figure.prototype.reset = function(duration) {
    this.axes.forEach(function(axes) {
        axes.reset();
    });
};

mpld3_Figure.prototype.enableLinkedBrush = function() {
    this.axes.forEach(function(axes) {
        axes.enableLinkedBrush();
    });
};

mpld3_Figure.prototype.disableLinkedBrush = function() {
    this.axes.forEach(function(axes) {
        axes.disableLinkedBrush();
    });
};

mpld3_Figure.prototype.enableBoxzoom = function() {
    this.axes.forEach(function(axes) {
        axes.enableBoxzoom();
    });
};

mpld3_Figure.prototype.disableBoxzoom = function() {
    this.axes.forEach(function(axes) {
        axes.disableBoxzoom();
    });
};

mpld3_Figure.prototype.enableZoom = function() {
    this.axes.forEach(function(axes) {
        axes.enableZoom();
    });
};

mpld3_Figure.prototype.disableZoom = function() {
    this.axes.forEach(function(axes) {
        axes.disableZoom();
    });
};

mpld3_Figure.prototype.toggleZoom = function() {
    if (this.isZoomEnabled) {
        this.disableZoom();
    } else {
        this.enableZoom();
    }
};

mpld3_Figure.prototype.setTicks = function(xy, nr, format) {
    this.axes.forEach(function(axes) {
        axes.setTicks(xy, nr, format);
    });
};

mpld3_Figure.prototype.setXTicks = function(nr, format) {
    this.setTicks('x', nr, format);
};

mpld3_Figure.prototype.setYTicks = function(nr, format) {
    this.setTicks('y', nr, format);
};

mpld3_Figure.prototype.removeNaN = function(data) {

    output = output.map(function(offsets){
      return offsets.map(function(value){
        if (typeof(value) == 'number' && isNaN(value)){
          return 0;
        } else {
          return value;
        }
      })
    })
};

mpld3_Figure.prototype.parse_offsets = function(data) {
    return data.map(function(offsets){
      return offsets.map(function(value){
        if (typeof(value) == 'number' && isNaN(value)){
          return 0;
        } else {
          return value;
        }
      })
    })
};

mpld3_Figure.prototype.get_data = function(data) {
    var output = data;
    if (data === null || typeof(data) === "undefined") {
        output = null;
    } else if (typeof(data) === "string") {
        output = this.data[data];
    }
    return output;
}
