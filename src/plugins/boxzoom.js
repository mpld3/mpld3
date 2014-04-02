import "base";
import "../toolbar/button"
import "../utils/icons"

/**********************************************************************/
/* BoxZoom Plugin */
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
    if (this.props.enabled === null){
        this.props.enabled = !(this.props.button);
    }

    var enabled = this.props.enabled;    
    if (this.props.button){
	// add a button to enable/disable box zoom
	var BoxZoomButton = mpld3.ButtonFactory({
	    buttonID: "boxzoom",
            sticky: true,
            actions: ["drag"],
	    onActivate: this.activate.bind(this),
	    onDeactivate: this.deactivate.bind(this),
            onDraw: function(){this.setState(enabled);},
	    icon: function(){return mpld3.icons["zoom"];},
	});
	this.fig.buttons.push(BoxZoomButton);
    }
    this.extentClass = "boxzoombrush";
}

mpld3_BoxZoomPlugin.prototype.activate = function(){
    if(this.enable) this.enable();
};

mpld3_BoxZoomPlugin.prototype.deactivate = function(){
    if(this.disable) this.disable();
};

mpld3_BoxZoomPlugin.prototype.draw = function(){
    mpld3.insert_css("#" + this.fig.figid + " rect.extent." + this.extentClass,
		     {"fill": "#fff",
                      "fill-opacity": 0,
                      "stroke": "#999"});
    
    // getBrush is a d3.svg.brush() object, set up for use on the figure.
    var brush = this.fig.getBrush();
    
    this.enable = function(){
        this.fig.showBrush(this.extentClass);
        brush.on("brushend", brushend.bind(this));
        this.enabled = true;
    }
    
    this.disable = function(){
        this.fig.hideBrush(this.extentClass);
        this.enabled = false;
    }
    
    this.toggle = function(){
	this.enabled ? this.disable() : this.enable();
    }
    
    function brushend(d, i){
	if(this.enabled){
	    var extent = brush.extent();
            if(extent[0][0] != extent[1][0] &&
               extent[0][1] != extent[1][1]){
		d.set_axlim([extent[0][0], extent[1][0]],
		            [extent[0][1], extent[1][1]]);
            }
	}
	d.axes.call(brush.clear());
    }
    this.disable();
}

