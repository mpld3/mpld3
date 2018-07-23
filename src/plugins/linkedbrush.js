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
    if (this.props.enabled === null) {
        this.props.enabled = !(this.props.button);
    }

    var enabled = this.props.enabled;
    if (this.props.button) {
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
    this.pathCollectionsByAxes = [];
    this.objectsByAxes = [];
    this.allObjects = [];
    this.extentClass = "linkedbrush";
    this.dataKey = 'offsets';
    this.objectClass = null;
}

mpld3_LinkedBrushPlugin.prototype.activate = function() {
    this.fig.enableLinkedBrush();
};

mpld3_LinkedBrushPlugin.prototype.deactivate = function() {
    this.fig.disableLinkedBrush();
};

mpld3_LinkedBrushPlugin.prototype.isPathInSelection = function(path, ix, iy, sel) {
    var result =
        sel[0][0] < path[ix] && sel[1][0] > path[ix] &&
        sel[0][1] < path[iy] && sel[1][1] > path[iy];
    return result;
};

mpld3_LinkedBrushPlugin.prototype.invertSelection = function(sel, axes) {
    var xs = [
        axes.x.invert(sel[0][0]),
        axes.x.invert(sel[1][0])
    ];
    var ys = [
        axes.y.invert(sel[1][1]),
        axes.y.invert(sel[0][1])
    ];
    return [
        [Math.min.apply(Math, xs), Math.min.apply(Math, ys)],
        [Math.max.apply(Math, xs), Math.max.apply(Math, ys)]
    ];
};

mpld3_LinkedBrushPlugin.prototype.update = function(selection) {
    if (!selection) {
        return;
    }

    this.pathCollectionsByAxes.forEach(function(axesColls, axesIndex) {
        var pathCollection = axesColls[0];
        var objects = this.objectsByAxes[axesIndex];

        var invertedSelection = this.invertSelection(selection, this.fig.axes[axesIndex]);
        var ix = pathCollection.props.xindex;
        var iy = pathCollection.props.yindex;

        objects.selectAll('path').classed('mpld3-hidden', function(path, idx) {
            return !this.isPathInSelection(path, ix, iy, invertedSelection);
        }.bind(this));
    }.bind(this));
};

mpld3_LinkedBrushPlugin.prototype.end = function() {
    this.allObjects.selectAll('path').classed('mpld3-hidden', false);
};

mpld3_LinkedBrushPlugin.prototype.draw = function() {
    // TODO: Ugh. Move this to some CSS somehow.
    mpld3.insert_css(
        '#' + this.fig.figid + ' path.mpld3-hidden',
        {
            'stroke': '#ccc !important',
            'fill': '#ccc !important'
        }
    );

    var pathCollection = mpld3.get_element(this.props.id);

    if (!pathCollection) {
        throw new Error('[LinkedBrush] Could not find path collection');
    }
    if (!('offsets' in pathCollection.props)) {
        throw new Error('[LinkedBrush] Figure is not a scatter plot.')
    }

    this.objectClass = 'mpld3-brushtarget-' + pathCollection.props[this.dataKey];

    this.pathCollectionsByAxes = this.fig.axes.map(function(axes) {
        return axes.elements.map(function(el) {
            if (el.props[this.dataKey] == pathCollection.props[this.dataKey]) {
                el.group.classed(this.objectClass, true);
                return el;
            }
        }.bind(this)).filter(function(d) { return d; });
    }.bind(this));

    this.objectsByAxes = this.fig.axes.map(function(axes) {
        return axes.axes.selectAll('.' + this.objectClass);
    }.bind(this));

    this.allObjects = this.fig.canvas.selectAll('.' + this.objectClass);
};
