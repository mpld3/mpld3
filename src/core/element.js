import "figure";
import "../utils/";

/**********************************************************************/
/* Base Object for Plot Elements */
mpld3.PlotElement = mpld3_PlotElement;

function mpld3_PlotElement(parent, props) {
    this.parent = isUndefinedOrNull(parent) ? null : parent;
    this.props = isUndefinedOrNull(props) ? {} : this.processProps(props);
    this.fig = (parent instanceof mpld3_Figure) ? parent :
        (parent && "fig" in parent) ? parent.fig : null;
    this.ax = (parent instanceof mpld3_Axes) ? parent :
        (parent && "ax" in parent) ? parent.ax : null;
}
mpld3_PlotElement.prototype.requiredProps = [];
mpld3_PlotElement.prototype.defaultProps = {};

mpld3_PlotElement.prototype.processProps = function(props) {
    // clone so that input is not overwritten
    props = mpld3_cloneObj(props);

    var finalProps = {};

    // Check that all required properties are specified
    var this_name = this.name();
    this.requiredProps.forEach(function(p) {
        if (!(p in props)) {
            throw ("property '" + p + "' " +
                "must be specified for " + this_name);
        }
        finalProps[p] = props[p];
        delete props[p];
    });

    // Use defaults where necessary
    for (var p in this.defaultProps) {
        if (p in props) {
            finalProps[p] = props[p];
            delete props[p];
        } else {
            finalProps[p] = this.defaultProps[p];
        }
    }

    // Assign ID, generating one if necessary
    if ("id" in props) {
        finalProps.id = props.id;
        delete props.id;
    } else if (!("id" in finalProps)) {
        finalProps.id = mpld3.generateId();
    }

    // Warn if there are any unrecognized properties
    for (var p in props) {
        console.warn("Unrecognized property '" + p + "' " +
            "for object " + this.name() + " (value = " + props[p] +
            ").");
    }
    return finalProps;
}

// Method to get the class name for console messages
mpld3_PlotElement.prototype.name = function() {
    var funcNameRegex = /function (.{1,})\(/;
    var results = (funcNameRegex).exec(this.constructor.toString());
    return (results && results.length > 1) ? results[1] : "";
};


