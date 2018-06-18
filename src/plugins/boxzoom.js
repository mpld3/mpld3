import "base";
import "../toolbar/button"
import "../utils/icons"


mpld3.BoxZoomPlugin = mpld3_BoxZoomPlugin;
mpld3.register_plugin("boxzoom", mpld3_BoxZoomPlugin);
mpld3_BoxZoomPlugin.prototype = Object.create(mpld3_Plugin.prototype);
mpld3_BoxZoomPlugin.prototype.constructor = mpld3_BoxZoomPlugin;
mpld3_BoxZoomPlugin.prototype.requiredProps = [];
mpld3_BoxZoomPlugin.prototype.defaultProps = {
    button: true,
    enabled: null
};

function mpld3_BoxZoomPlugin(fig, props) {
    mpld3_Plugin.call(this, fig, props);
    if (this.props.enabled === null) {
        this.props.enabled = !(this.props.button);
    }

    var enabled = this.props.enabled;
    if (this.props.button) {
        // add a button to enable/disable box zoom
        var BoxZoomButton = mpld3.ButtonFactory({
            buttonID: "boxzoom",
            sticky: true,
            actions: ["drag"],
            onActivate: this.activate.bind(this),
            onDeactivate: this.deactivate.bind(this),
            onDraw: function() { this.setState(enabled); },
            icon: function() { return mpld3.icons["zoom"]; },
        });
        this.fig.buttons.push(BoxZoomButton);
    }
    this.extentClass = "boxzoombrush";
}

mpld3_BoxZoomPlugin.prototype.activate = function() {
    // TODO: (@vladh) Multiple axes.
    this.brushG = this.fig.axes[0].axes
        .append('g')
        .attr('class', 'brush')
        .call(this.brush);
    this.fig.enableZoom();
};

mpld3_BoxZoomPlugin.prototype.deactivate = function() {
    if (this.brushG) {
        this.brushG.remove();
        this.brushG.on('.brush', null);
    }
    this.fig.disableZoom();
};

mpld3_BoxZoomPlugin.prototype.draw = function() {
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
};

mpld3_BoxZoomPlugin.prototype.brushStart = function() {
};

// Sorry for this function name.
mpld3_BoxZoomPlugin.prototype.brushBrush = function() {
};

mpld3_BoxZoomPlugin.prototype.brushEnd = function() {
    if (!d3.event.selection || !this.fig.canvas || !this.brushG) {
        return;
    }

    var bounds = d3.event.selection;
    var width = this.fig.width;
    var height = this.fig.height;

    var dx = bounds[1][0] - bounds[0][0];
    var dy = bounds[1][1] - bounds[0][1];
    var x = (bounds[0][0] + bounds[1][0]) / 2;
    var y = (bounds[0][1] + bounds[1][1]) / 2;
    var scale = Math.max(1, Math.min(8, 0.9 / Math.max(dx / width, dy / height)));
    var translate = [width / 2 - scale * x, height / 2 - scale * y];

    this.brushG.call(this.brush.move, null);
    this.fig.axes[0].axes.transition()
        .duration(750)
        .call(
            this.fig.zoom.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
        );
};
