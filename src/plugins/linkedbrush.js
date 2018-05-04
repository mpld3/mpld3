import "base";
import "../toolbar/button"
import "../utils/icons"

mpld3.LinkedBrushPlugin = mpld3_LinkedBrushPlugin;
mpld3.register_plugin("linkedbrush", mpld3_LinkedBrushPlugin);
mpld3_LinkedBrushPlugin.prototype = Object.create(mpld3.Plugin.prototype);
mpld3_LinkedBrushPlugin.prototype.constructor = mpld3_LinkedBrushPlugin;
mpld3_LinkedBrushPlugin.prototype.requiredProps = ["id"];
mpld3_LinkedBrushPlugin.prototype.defaultProps = {
    button: true,
    enabled: null
};

function mpld3_LinkedBrushPlugin(fig, props){
    mpld3.Plugin.call(this, fig, props);
    if (this.props.enabled === null){
        this.props.enabled = !(this.props.button);
    }

    var enabled = this.props.enabled;
    if (this.props.button){
        var BrushButton = mpld3.ButtonFactory({
            buttonID: "linkedbrush",
            sticky: true,
            actions: ["drag"],
            onActivate: this.activate.bind(this),
            onDeactivate: this.deactivate.bind(this),
            onDraw: function(){this.setState(enabled);},
            icon: function(){return mpld3.icons["brush"];},
        });
        this.fig.buttons.push(BrushButton);
    }
    this.extentClass = "linkedbrush";
}

mpld3_LinkedBrushPlugin.prototype.activate = function(){
    if(this.enable) this.enable();
};

mpld3_LinkedBrushPlugin.prototype.deactivate = function(){
    if(this.disable) this.disable();
};

mpld3_LinkedBrushPlugin.prototype.draw = function(){
    // TODO: (@vladh) Fix brush in LinkedBrushPlugin.
    return undefined;
    var obj = mpld3.get_element(this.props.id);
    if(obj === null){
        throw("LinkedBrush: no object with id='"
              + this.props.id + "' was found");
    }
    var fig = this.fig;
    if(!("offsets" in obj.props)){
        throw("Plot object with id='" + this.props.id
              + "' is not a scatter plot");
    }
    var dataKey = ("offsets" in obj.props) ? "offsets" : "data";

    mpld3.insert_css("#" + fig.figid + " rect.extent." + this.extentClass,
                     {"fill": "#000",
                      "fill-opacity": .125,
                      "stroke": "#fff"});

    mpld3.insert_css("#" + fig.figid + " path.mpld3-hidden",
                     {"stroke": "#ccc !important",
                      "fill": "#ccc !important"});

    var dataClass = "mpld3data-" + obj.props[dataKey];
    var brush = fig.getBrush();

    // Label all data points & find data in each axes
    var dataByAx = [];
    fig.axes.forEach(function(ax){
        var axData = [];
        ax.elements.forEach(function(el){
            if(el.props[dataKey] === obj.props[dataKey]){
                el.group.classed(dataClass, true);
                axData.push(el);
            }
        });
        dataByAx.push(axData);
    });

    // For fast brushing, precompute a list of selection properties
    // properties to apply to the selction.
    var allData = [];
    var dataToBrush = fig.canvas.selectAll("." + dataClass);
    var currentAxes;

    function brushstart(d){
        if(currentAxes != this){
            d3.select(currentAxes).call(brush.clear());
            currentAxes = this;
            brush.x(d.xdom).y(d.ydom);
        }
    }

    function brushmove(d){
        var data = dataByAx[d.axnum];
        if(data.length > 0){
            var ix = data[0].props.xindex;
            var iy = data[0].props.yindex;
            var e = brush.extent();
            if (brush.empty()){
                dataToBrush.selectAll("path").classed("mpld3-hidden", false);
            } else {
                dataToBrush.selectAll("path")
                           .classed("mpld3-hidden",
                              function(p) {
                                  return e[0][0] > p[ix] || e[1][0] < p[ix] ||
                                         e[0][1] > p[iy] || e[1][1] < p[iy];
                              });
            }
        }
    }

    function brushend(d){
        if (brush.empty()){
            dataToBrush.selectAll("path").classed("mpld3-hidden", false);
        }
    }

    this.enable = function(){
      this.fig.showBrush(this.extentClass);
      brush.on("brushstart", brushstart)
           .on("brush", brushmove)
           .on("brushend", brushend);
      this.enabled = true;
    }

    this.disable = function(){
        d3.select(currentAxes).call(brush.clear());
        this.fig.hideBrush(this.extentClass);
        this.enabled = false;
    }

    this.disable();
}
