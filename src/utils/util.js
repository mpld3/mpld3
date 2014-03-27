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