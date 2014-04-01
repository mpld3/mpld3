import "base";
import "../toolbar/button";
import "../utils/icons";

/**********************************************************************/
/* Reset Plugin */
mpld3.ResetPlugin = mpld3_ResetPlugin;
mpld3.register_plugin("reset", mpld3_ResetPlugin);
mpld3_ResetPlugin.prototype = Object.create(mpld3_Plugin.prototype);
mpld3_ResetPlugin.prototype.constructor = mpld3_ResetPlugin;
mpld3_ResetPlugin.prototype.requiredProps = [];
mpld3_ResetPlugin.prototype.defaultProps = {};

function mpld3_ResetPlugin(fig, props) {
    mpld3_Plugin.call(this, fig, props);
    var ResetButton = mpld3.ButtonFactory({
        buttonID: "reset",
        sticky: false,
        onActivate: function() {
            this.toolbar.fig.reset();
        },
        icon: function() {
            return mpld3.icons["reset"];
        }
    });
    this.fig.buttons.push(ResetButton);
}
