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

mpld3_BoxZoomPlugin.prototype.activate = function(){
    if (this.enable) this.enable();
};

mpld3_BoxZoomPlugin.prototype.deactivate = function(){
    if (this.disable) this.disable();
};

mpld3_BoxZoomPlugin.prototype.draw = function(){
    // TODO: (@vladh) [brush] Fix brush in boxzoom.
    mpld3.insert_css(
        "#" + this.fig.figid + " rect.extent." + this.extentClass,
        {
            "fill": "#fff",
            "fill-opacity": 0,
            "stroke": "#999",
        }
    );

    // getBrush is a d3.brush() object, set up for use on the figure.
    var brush = this.fig.getBrush();

    this.enable = function() {
        console.log('[boxzoom#enable]');
        this.fig.showBrush(this.extentClass);
        brush.on("end", brushend.bind(this));
        this.enabled = true;
    }

    this.disable = function() {
        console.log('[boxzoom#disable]');
        this.fig.hideBrush(this.extentClass);
        this.enabled = false;
    }

    this.toggle = function() {
        console.log('[boxzoom#toggle] enabled:', this.enabled);
        this.enabled ? this.disable() : this.enable();
    }

    function brushend(d) {
        console.log('[boxboxzoom#brushend]', extent);
        var extent = d3.event.selection;
        if (!extent) {
            console.log('[boxboxzoom#brushend] doing nothing');
            return;
        }
        console.log('[boxboxzoom#brushend] trying to do something');
        if (this.enabled) {
            console.log('[boxboxzoom#brushend] doing something');
            d.set_axlim(
                [extent[0][0], extent[1][0]],
                [extent[0][1], extent[1][1]],
                null,
                null,
                extent
            );
        }
        d.axes.call(brush.move, null);
    }

    this.disable();
}

