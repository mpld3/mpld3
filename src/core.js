/**********************************************************************/
/* Base Object for Plot Elements */
mpld3.PlotElement = mpld3_PlotElement;

function mpld3_PlotElement(parent, props) {
    this.parent = parent;
    if (typeof props !== "undefined")
        this.props = this.processProps(props);
    this.fig = (parent instanceof mpld3_Figure) ? parent :
        (parent && "fig" in parent) ? parent.fig : null;
    this.ax = (parent instanceof mpld3_Axes) ? parent :
        (parent && "ax" in parent) ? parent.ax : null;
}
mpld3_PlotElement.prototype.requiredProps = [];
mpld3_PlotElement.prototype.defaultProps = {};

mpld3_PlotElement.prototype.processProps = function(props) {
    finalProps = {};

    // Check that all required properties are specified
    this.requiredProps.forEach(function(p) {
        if (!(p in props)) {
            throw ("property '" + p + "' " +
                "must be specified for " + this.name());
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



/**********************************************************************/
/* Button object: */
mpld3.Button = mpld3_Button;
mpld3_Button.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Button.prototype.constructor = mpld3_Button;

function mpld3_Button(toolbar, key) {
    mpld3_PlotElement.call(this, toolbar);
    this.toolbar = toolbar;
    this.cssclass = "mpld3-" + key + "button";
    this.active = false;
}

mpld3_Button.prototype.click = function() {
    this.active ? this.deactivate() : this.activate();
};

mpld3_Button.prototype.activate = function() {
    this.toolbar.deactivate_by_action(this.actions);
    this.onActivate();
    this.active = true;
    this.toolbar.toolbar.select('.' + this.cssclass)
        .classed({
            pressed: true
        });
    if (!this.sticky)
        this.deactivate();
};

mpld3_Button.prototype.deactivate = function() {
    this.onDeactivate();
    this.active = false;
    this.toolbar.toolbar.select('.' + this.cssclass)
        .classed({
            pressed: false
        });
}
mpld3_Button.prototype.sticky = false;
mpld3_Button.prototype.actions = [];
mpld3_Button.prototype.icon = function() {
    return "";
}
mpld3_Button.prototype.onActivate = function() {};
mpld3_Button.prototype.onDeactivate = function() {};
mpld3_Button.prototype.onDraw = function() {};

/* Factory for button classes */
mpld3.ButtonFactory = function(members) {
    function B(toolbar, key) {
        mpld3_Button.call(this, toolbar, key);
    };
    B.prototype = Object.create(mpld3_Button.prototype);
    B.prototype.constructor = B;
    for (key in members) B.prototype[key] = members[key];
    mpld3.Toolbar.prototype.buttonDict[members.toolbarKey] = B;
    return B;
}

/* Reset Button */
mpld3.ResetButton = mpld3.ButtonFactory({
    toolbarKey: "reset",
    sticky: false,
    onActivate: function() {
        this.toolbar.fig.reset();
    },
    icon: function() {
        return mpld3.icons["reset"];
    }
});

/* Move Button */
mpld3.MoveButton = mpld3.ButtonFactory({
    toolbarKey: "move",
    sticky: true,
    actions: ["scroll", "drag"],
    onActivate: function() {
        this.toolbar.fig.enable_zoom();
    },
    onDeactivate: function() {
        this.toolbar.fig.disable_zoom();
    },
    onDraw: function() {
        this.toolbar.fig.disable_zoom();
    },
    icon: function() {
        return mpld3.icons["move"];
    }
});

/***********************************************************************/
/* Coordinates Object: Converts from given units to screen/pixel units */
/*   `trans` is one of ["data", "figure", "axes", "display"]           */
mpld3.Coordinates = mpld3_Coordinates;

function mpld3_Coordinates(trans, ax) {
    if (typeof(ax) === "undefined") {
        this.ax = null;
        this.fig = null;
        if (this.trans !== "display")
            throw "ax must be defined if transform != 'display'";
    } else {
        this.ax = ax;
        this.fig = ax.fig;
    }
    this.zoomable = (trans === "data");
    this.x = this["x_" + trans];
    this.y = this["y_" + trans];
    if (typeof(this.x) === "undefined" || typeof(this.y) === "undefined")
        throw "unrecognized coordinate code: " + trans;
}

mpld3_Coordinates.prototype.xy = function(d, ix, iy) {
    ix = (typeof(ix) === "undefined") ? 0 : ix;
    iy = (typeof(iy) === "undefined") ? 1 : iy;
    return [this.x(d[ix]), this.y(d[iy])];
};

mpld3_Coordinates.prototype.x_data = function(x) {
    return this.ax.x(x);
}
mpld3_Coordinates.prototype.y_data = function(y) {
    return this.ax.y(y);
}
mpld3_Coordinates.prototype.x_display = function(x) {
    return x;
}
mpld3_Coordinates.prototype.y_display = function(y) {
    return y;
}
mpld3_Coordinates.prototype.x_axes = function(x) {
    return x * this.ax.width;
}
mpld3_Coordinates.prototype.y_axes = function(y) {
    return this.ax.height * (1 - y);
}
mpld3_Coordinates.prototype.x_figure = function(x) {
    return x * this.fig.width - this.ax.position[0];
}
mpld3_Coordinates.prototype.y_figure = function(y) {
    return (1 - y) * this.fig.height - this.ax.position[1];
}


/**********************************************************************/
/* Data Parsing Functions */
mpld3.draw_figure = function(figid, spec) {
    var element = document.getElementById(figid);
    if (element === null) {
        throw (figid + " is not a valid id");
        return null;
    }
    var fig = new mpld3.Figure(figid, spec);
    mpld3.figures.push(fig);
    fig.draw();
    return fig;
};


/**********************************************************************/
/* Convenience Functions                                              */

mpld3.merge_objects = function(_) {
    var output = {};
    var obj;
    for (var i = 0; i < arguments.length; i++) {
        obj = arguments[i];
        for (var attr in obj) {
            output[attr] = obj[attr];
        }
    }
    return output;
}

mpld3.generate_id = function(N, chars) {
    console.warn("mpld3.generate_id is deprecated. " +
        "Use mpld3.generateId instead.")
    return mpld3_generateId(N, chars);
}

mpld3.generateId = mpld3_generateId;

function mpld3_generateId(N, chars) {
    N = (typeof(N) !== "undefined") ? N : 10;
    chars = (typeof(chars) !== "undefined") ? chars :
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    var id = "";
    for (var i = 0; i < N; i++)
        id += chars.charAt(Math.round(Math.random() * (chars.length - 1)));
    return id;
}

// TODO: should elements be stored in a map/hash table instead?
// It would make this more efficient.
mpld3.get_element = function(id, fig) {
    var figs_to_search, ax, el;
    if (typeof(fig) === "undefined") {
        figs_to_search = mpld3.figures;
    } else if (typeof(fig.length) === "undefined") {
        figs_to_search = [fig];
    } else {
        figs_to_search = fig;
    }
    for (var i = 0; i < figs_to_search.length; i++) {
        fig = figs_to_search[i];
        if (fig.props.id === id) {
            return fig;
        }
        for (var j = 0; j < fig.axes.length; j++) {
            ax = fig.axes[j];
            if (ax.props.id === id) {
                return ax;
            }
            for (var k = 0; k < ax.elements.length; k++) {
                el = ax.elements[k];
                if (el.props.id === id) {
                    return el;
                }
            }
        }
    }
    return null;
}

// Function to insert some CSS into the header
mpld3.insert_css = function(selector, attributes) {
    var head = document.head || document.getElementsByTagName('head')[0];
    var style = document.createElement('style');

    var css = selector + " {"
    for (var prop in attributes) {
        css += prop + ":" + attributes[prop] + "; "
    }
    css += "}"

    style.type = 'text/css';
    if (style.styleSheet) {
        style.styleSheet.cssText = css;
    } else {
        style.appendChild(document.createTextNode(css));
    }
    head.appendChild(style);
};

// needed for backward compatibility
mpld3.process_props = function(obj, properties, defaults, required) {
    console.warn("mpld3.process_props is deprecated. " +
        "Plot elements should derive from mpld3.PlotElement");
    Element.prototype = Object.create(mpld3_PlotElement.prototype);
    Element.prototype.constructor = Element
    Element.prototype.requiredProps = required;
    Element.prototype.defaultProps = defaults;

    function Element(props) {
        mpld3_PlotElement.call(this, null, props);
    }
    var el = new Element(properties);
    return el.props;
};

mpld3.interpolateDates = mpld3_interpolateDates;

function mpld3_interpolateDates(a, b) {
    var interp = d3.interpolate([a[0].valueOf(), a[1].valueOf()], [b[0].valueOf(), b[1].valueOf()])
    return function(t) {
            var i = interp(t);
            return [new Date(i[0]), new Date(i[1])];
        }
}

function isUndefined(x) {
    return (typeof(x) === "undefined");
}

function isUndefinedOrNull(x) {
    return (x == null || isUndefined(x));
}

function getMod(L, i) {
    return (L.length > 0) ? L[i % L.length] : null;
}

function mpld3_path(_) {
    var x = function(d, i) {
        return d[0];
    };
    var y = function(d, i) {
        return d[1];
    };
    var defined = function(d, i) {
        return true;
    };

    // number of vertices for each SVG code
    var n_vertices = {
        M: 1,
        m: 1,
        L: 1,
        l: 1,
        Q: 2,
        q: 2,
        T: 1,
        t: 1,
        S: 2,
        s: 2,
        C: 3,
        c: 3,
        Z: 0,
        z: 0
    };

    function path(vertices, pathcodes) {
        var fx = d3.functor(x),
            fy = d3.functor(y);
        var points = [],
            segments = [],
            i_v = 0,
            i_c = -1,
            halt = 0,
            nullpath = false;

        // If pathcodes is not defined, use straight line segments
        if (!pathcodes) {
            pathcodes = ["M"];
            for (var i = 1; i < vertices.length; i++) pathcodes.push("L");
        }

        while (++i_c < pathcodes.length) {
            halt = i_v + n_vertices[pathcodes[i_c]];
            points = [];
            while (i_v < halt) {
                if (defined.call(this, vertices[i_v], i_v)) {
                    points.push(fx.call(this, vertices[i_v], i_v),
                        fy.call(this, vertices[i_v], i_v));
                    i_v++;
                } else {
                    points = null;
                    i_v = halt;
                }
            }

            if (!points) {
                nullpath = true;
            } else if (nullpath && points.length > 0) {
                segments.push("M", points[0], points[1]);
                nullpath = false;
            } else {
                segments.push(pathcodes[i_c]);
                segments = segments.concat(points);
            }
        }
        if (i_v != vertices.length)
            console.warn("Warning: not all vertices used in Path");
        return segments.join(" ");
    }

    path.x = function(_) {
        if (!arguments.length) return x;
        x = _;
        return path;
    };

    path.y = function(_) {
        if (!arguments.length) return y;
        y = _;
        return path;
    };

    path.defined = function(_) {
        if (!arguments.length) return defined;
        defined = _;
        return path;
    };

    path.call = path;

    return path;
}

mpld3.path = function() {
    return mpld3_path();
}

mpld3.icons = {
    reset: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\nWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gIcACMoD/OzIwAAAJhJREFUOMtjYKAx4KDUgNsMDAx7\nyNV8i4GB4T8U76VEM8mGYNNMtCH4NBM0hBjNMIwSsMzQ0MamcDkDA8NmQi6xggpUoikwQbIkHk2u\nE0rLI7vCBknBSyxeRDZAE6qHgQkq+ZeBgYERSfFPAoHNDNUDN4BswIRmKgxwEasP2dlsDAwMYlA/\n/mVgYHiBpkkGKscIDaPfVMmuAGnOTaGsXF0MAAAAAElFTkSuQmCC\n",
    move: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\nWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gIcACQMfLHBNQAAANZJREFUOMud07FKA0EQBuAviaKB\nlFr7COJrpAyYRlKn8hECEkFEn8ROCCm0sBMRYgh5EgVFtEhsRjiO27vkBoZd/vn5d3b+XcrjFI9q\nxgXWkc8pUjOB93GMd3zgB9d1unjDSxmhWSHQqOJki+MtOuv/b3ZifUqctIrMxwhHuG1gim4Ma5kR\nWuEkXFgU4B0MW1Ho4TeyjX3s4TDq3zn8ALvZ7q5wX9DqLOHCDA95cFBAnOO1AL/ZdNopgY3fQcqF\nyriMe37hM9w521ZkkvlMo7o/8g7nZYQ/QDctp1nTCf0AAAAASUVORK5CYII=\n"
};
