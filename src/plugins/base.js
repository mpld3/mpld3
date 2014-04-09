import "../core/element";


/**********************************************************************/
/* Plugin Base Class */
mpld3.Plugin = mpld3_Plugin;
mpld3_Plugin.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Plugin.prototype.constructor = mpld3_Plugin;
mpld3_Plugin.prototype.requiredProps = [];
mpld3_Plugin.prototype.defaultProps = {};

function mpld3_Plugin(fig, props){
    mpld3_PlotElement.call(this, fig, props);
};

mpld3_Plugin.prototype.draw = function(){};
