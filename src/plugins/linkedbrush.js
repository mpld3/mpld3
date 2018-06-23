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

function mpld3_LinkedBrushPlugin(fig, props) {
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
            onDraw: function(){ this.setState(enabled); },
            icon: function(){ return mpld3.icons["brush"]; },
        });
        this.fig.buttons.push(BrushButton);
    }
    this.dataByAxes = [];
    this.extentClass = "linkedbrush";
    this.dataKey = 'offsets';
    this.objectClass = null;
}

mpld3_LinkedBrushPlugin.prototype.activate = function() {
    this.brushG = this.fig.canvas
        .append('g')
        .attr('class', 'brush')
        .call(this.brush);
};

mpld3_LinkedBrushPlugin.prototype.deactivate = function() {
    if (this.brushG) {
        this.brushG.remove();
        this.brushG.on('.brush', null);
    }
};

mpld3_LinkedBrushPlugin.prototype.isPathInSelection = function(path, ix, iy, sel) {
    var result =
        sel[0][0] < path[ix] && sel[1][0] > path[ix] &&
        sel[0][1] < path[iy] && sel[1][1] > path[iy];
    return result;
};

mpld3_LinkedBrushPlugin.prototype.invertSelection = function(sel, axes) {
    return [
        [axes.x.invert(sel[0][0]), axes.y.invert(sel[0][1])],
        [axes.x.invert(sel[1][0]), axes.y.invert(sel[1][1])]
    ];
};

// Sorry for this function name.
mpld3_LinkedBrushPlugin.prototype.brushBrush = function() {
    var selection = d3.event.selection;
    if (!selection) {
        this.objects.selectAll('path').classed('mpld3-hidden', false);
        return;
    }

    this.dataByAxes.forEach(function(axesData, index) {
        var invertedSelection = this.invertSelection(selection, this.fig.axes[index]);
        console.log(invertedSelection);
        var ix = axesData[0].props.xindex;
        var iy = axesData[0].props.yindex;

        // TODO: (@vladh) Only go through the elements of these axes.
        this.objects.selectAll('path')
            .classed('mpld3-hidden', function(path) {
                return !this.isPathInSelection(path, ix, iy, invertedSelection);
            }.bind(this));
    }.bind(this));
};

mpld3_LinkedBrushPlugin.prototype.brushEnd = function() {
    if (!d3.event.selection) {
        this.objects.selectAll('path').classed('mpld3-hidden', false);
    }
};

mpld3_LinkedBrushPlugin.prototype.draw = function() {
    // Ugh.
    mpld3.insert_css(
        '#' + this.fig.figid + ' path.mpld3-hidden',
        {
            'stroke': '#ccc !important',
            'fill': '#ccc !important'
        }
    );

    this.brush = d3.brush().extent([
        [0, 0], [this.fig.width, this.fig.height],
    ])
        .on('brush', this.brushBrush.bind(this))
        .on('end', this.brushEnd.bind(this));

    var pathCollection = mpld3.get_element(this.props.id);

    if (!pathCollection) {
        throw new Error('[LinkedBrush] Could not find path collection');
    }
    if (!('offsets' in pathCollection.props)) {
        throw new Error('[LinkedBrush] Figure is not a scatter plot.')
    }

    this.objectClass = 'mpld3-brushtarget-' + pathCollection.props[this.dataKey];

    this.dataByAxes = this.fig.axes.map(function(axes) {
        return axes.elements.map(function(el) {
            if (el.props[this.dataKey] == pathCollection.props[this.dataKey]) {
                el.group.classed(this.objectClass, true);
                return el;
            }
        }.bind(this)).filter(function(d) { return d; });
    }.bind(this));

    this.objects = this.fig.canvas.selectAll('.' + this.objectClass);
};
