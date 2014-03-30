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
    enabled: true,
};

function mpld3_BoxZoomPlugin(fig, props) {
    mpld3_Plugin.call(this, fig, props);
    
    if (this.props.button){
	// add a button to enable/disable box zoom
	mpld3.ButtonFactory({
	    toolbarKey: "boxzoom",
            sticky: true,
            actions: ["drag"],
	    onActivate: this.activate.bind(this),
	    onDeactivate: this.deactivate.bind(this),
            onDraw: this.deactivate.bind(this),
	    icon: function(){return mpld3.icons["zoom"];},
	});
	this.fig.props.buttons.push("boxzoom");
    }
}

mpld3_BoxZoomPlugin.prototype.activate = function(){
    if(this.enable) this.enable();
};

mpld3_BoxZoomPlugin.prototype.deactivate = function(){
    if(this.disable) this.disable();
};

mpld3_BoxZoomPlugin.prototype.draw = function(){
    mpld3.insert_css("#" + this.fig.figid + " rect.extent",
		     {"fill": "#fff",
                      "fill-opacity": 0,
                      "stroke": "#999"});
    
    var brush = d3.svg.brush()
	.x(this.fig.axes[0].x)
        .y(this.fig.axes[0].y)
        .on("brushend", brushend.bind(this));
    
    this.fig.root.selectAll(".mpld3-axes")
	.data(this.fig.axes)
	.call(brush)
    
    this.enable = function(){
        brush.on("brushstart", brushstart);
        this.fig.canvas.selectAll("rect.background")
	    .style("cursor", "crosshair");
        this.fig.canvas.selectAll("rect.extent, rect.resize")
	    .style("display", null);
        this.enabled = true;
    }
    
    this.disable = function(){
        brush.on("brushstart", null).clear();
        this.fig.canvas.selectAll("rect.background")
	    .style("cursor", null);
        this.fig.canvas.selectAll("rect.extent, rect.resize")
	    .style("display", "none");
        this.enabled = false;
    }
    
    this.toggle = function(){
	this.enabled ? this.disable() : this.enable();
    }
    
    function brushstart(d, i){
	brush.x(d.x).y(d.y);
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

    if(this.props.enabled){
	this.enable();
    }else{
	this.disable();
    }
}    

