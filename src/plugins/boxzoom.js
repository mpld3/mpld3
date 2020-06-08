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
    this.fig.enableBoxzoom();
};

mpld3_BoxZoomPlugin.prototype.deactivate = function() {
    this.fig.disableBoxzoom();
};

mpld3_BoxZoomPlugin.prototype.draw = function() {
    if (this.props.enabled) {
      this.activate();
    } else {
      this.deactivate();
    }
};
