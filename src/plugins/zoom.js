import "base";
import "../toolbar/button"
import "../utils/icons"

/**********************************************************************/
/* Zoom Plugin */
mpld3.ZoomPlugin = mpld3_ZoomPlugin;
mpld3.register_plugin("zoom", mpld3_ZoomPlugin);
mpld3_ZoomPlugin.prototype = Object.create(mpld3_Plugin.prototype);
mpld3_ZoomPlugin.prototype.constructor = mpld3_ZoomPlugin;
mpld3_ZoomPlugin.prototype.requiredProps = [];
mpld3_ZoomPlugin.prototype.defaultProps = {
    button: true,
    enabled: null
};

function mpld3_ZoomPlugin(fig, props) {
    mpld3_Plugin.call(this, fig, props);
    if (this.props.enabled === null) {
        this.props.enabled = !(this.props.button);
    }

    var enabled = this.props.enabled;

    if (this.props.button) {
        var ZoomButton = mpld3.ButtonFactory({
            buttonID: "zoom",
            sticky: true,
            actions: ["scroll", "drag"],
            onActivate: this.activate.bind(this),
            onDeactivate: this.deactivate.bind(this),
            onDraw: function() { this.setState(enabled); },
            icon: function() {
                return mpld3.icons["move"];
            }
        });
        this.fig.buttons.push(ZoomButton);
    }
}

mpld3_ZoomPlugin.prototype.activate = function() {
    this.fig.enableZoom();
};

mpld3_ZoomPlugin.prototype.deactivate = function() {
    this.fig.disableZoom()
};

mpld3_ZoomPlugin.prototype.draw = function() {
    if (this.props.enabled) {
      this.activate();
    } else {
      this.deactivate();
    }
}
