import "base";
import "../toolbar/button";
import "../utils/icons";

/**********************************************************************/
/* Mouse Position Plugin */

mpld3.register_plugin("mouseposition", MousePositionPlugin);
MousePositionPlugin.prototype = Object.create(mpld3.Plugin.prototype);
MousePositionPlugin.prototype.constructor = MousePositionPlugin;
MousePositionPlugin.prototype.requiredProps = [];
MousePositionPlugin.prototype.defaultProps = {fontsize: 12, fmt: ".3g"};
function MousePositionPlugin(fig, props){
    mpld3.Plugin.call(this, fig, props);
};

MousePositionPlugin.prototype.draw = function(){
    var fig = this.fig;
    var fmt = d3.format(this.props.fmt);
    var coords = fig.canvas.append("text")
                    .attr("class", "mpld3-coordinates")
                    .style("text-anchor", "end")
                    .style("font-size", this.props.fontsize)
                    .attr("x", this.fig.width - 5)
                    .attr("y", this.fig.height - 5);

    for (var i=0; i < this.fig.axes.length; i++) {
      var update_coords = function() {
            var ax = fig.axes[i];
            return function() {
              var pos = d3.mouse(this),
                  x = ax.x.invert(pos[0]),
                  y = ax.y.invert(pos[1]);
              coords.text("(" + fmt(x) + ", " + fmt(y) + ")");
            };
          }();
      fig.axes[i].baseaxes
        .on("mousemove", update_coords)
        .on("mouseout", function() { coords.text(""); });
    }
};
