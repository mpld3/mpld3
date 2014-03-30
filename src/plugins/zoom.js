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
    type: "zoom",
    button: true,
    enabled: null
};

function mpld3_ZoomPlugin(fig, props) {
    mpld3_Plugin.call(this, fig, props);
    
    if (this.props.button){
        mpld3.ButtonFactory({
            toolbarKey: "zoom",
            sticky: true,
            actions: ["scroll", "drag"],
            onActivate: function() {
                this.fig.enable_zoom();
            },
            onDeactivate: function() {
                this.fig.disable_zoom();
            },
            icon: function() {
                return mpld3.icons["move"];
            }
        });
	this.fig.props.buttons.push("zoom");
    }	
    if (this.props.enabled === null){
        this.props.enabled = !(this.props.button);
    }
}

mpld3_ZoomPlugin.prototype.draw = function(){
    if(this.props.enabled){
        this.fig.enable_zoom();
    }else{
	this.fig.disable_zoom();
    }
}
