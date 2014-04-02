import "base";

/**********************************************************************/
/* Tooltip Plugin */
mpld3.TooltipPlugin = mpld3_TooltipPlugin;
mpld3.register_plugin("tooltip", mpld3_TooltipPlugin);
mpld3_TooltipPlugin.prototype = Object.create(mpld3_Plugin.prototype);
mpld3_TooltipPlugin.prototype.constructor = mpld3_TooltipPlugin;
mpld3_TooltipPlugin.prototype.requiredProps = ["id"];
mpld3_TooltipPlugin.prototype.defaultProps = {
    labels: null,
    hoffset: 0,
    voffset: 10,
    location: 'mouse'
};

function mpld3_TooltipPlugin(fig, props) {
    mpld3_Plugin.call(this, fig, props);
}

mpld3_TooltipPlugin.prototype.draw = function() {
    var obj = mpld3.get_element(this.props.id, this.fig);
    var labels = this.props.labels;
    var loc = this.props.location;

    this.tooltip = this.fig.canvas.append("text")
        .attr("class", "mpld3-tooltip-text")
        .attr("x", 0)
        .attr("y", 0)
        .text("")
        .style("visibility", "hidden");

    if (loc == "bottom left" || loc == "top left") {
        this.x = obj.ax.position[0] + 5 + this.props.hoffset;
        this.tooltip.style("text-anchor", "beginning")
    } else if (loc == "bottom right" || loc == "top right") {
        this.x = obj.ax.position[0] + obj.ax.width - 5 + this.props.hoffset;
        this.tooltip.style("text-anchor", "end");
    } else {
        this.tooltip.style("text-anchor", "middle");
    }

    if (loc == "bottom left" || loc == "bottom right") {
        this.y = obj.ax.position[1] + obj.ax.height - 5 + this.props.voffset;
    } else if (loc == "top left" || loc == "top right") {
        this.y = obj.ax.position[1] + 5 + this.props.voffset;
    }

    function mouseover(d, i) {
        this.tooltip
            .style("visibility", "visible")
            .text((labels === null) ? "(" + d + ")" : getMod(labels, i));
    }

    function mousemove(d, i) {
        if (loc === "mouse") {
            var pos = d3.mouse(this.fig.canvas.node())
            this.x = pos[0] + this.props.hoffset;
            this.y = pos[1] - this.props.voffset;
        }

        this.tooltip
            .attr('x', this.x)
            .attr('y', this.y);
    }

    function mouseout(d, i) {
        this.tooltip.style("visibility", "hidden");
    }

    obj.elements()
        .on("mouseover", mouseover.bind(this))
        .on("mousemove", mousemove.bind(this))
        .on("mouseout", mouseout.bind(this));
}