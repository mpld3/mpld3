/**********************************************************************/
/* Plugin registry */
mpld3.register_plugin = function(name, obj){
    mpld3.plugin_map[name] = obj;
};

/**********************************************************************/
/* Remove root figure from mpld3.figure */
mpld3.remove_figure = function(figid) {
    var element = document.getElementById(figid);
    if (element !== null) {
      element.innerHTML = '';
    }
    for (var i = 0; i < mpld3.figures.length; i++) {
        var fig = mpld3.figures[i];
        if (fig.figid === figid) {
          mpld3.figures.splice(i, 1);
        }
    }
    return true;
}

/**********************************************************************/
/* Data Parsing Functions */
mpld3.draw_figure = function(figid, spec, process, clearElem) {
    var element = document.getElementById(figid);
    clearElem = typeof clearElem !== 'undefined' ? clearElem : false;
    if (clearElem){
      mpld3.remove_figure(figid);
    }
    if (element === null) {
        throw (figid + " is not a valid id");
    }
    var fig = new mpld3.Figure(figid, spec);
    if (process) {
        process(fig, element);
    }
    mpld3.figures.push(fig);
    fig.draw();
    return fig;
};


/**********************************************************************/
/* Convenience Functions                                              */

mpld3.cloneObj = mpld3_cloneObj;

function mpld3_cloneObj(oldObj) {
   var newObj = {};
   for(var key in oldObj){
       newObj[key] = oldObj[key];
   }
   return newObj;
}

mpld3.boundsToTransform = function(fig, bounds) {
    // https://bl.ocks.org/iamkevinv/0a24e9126cd2fa6b283c6f2d774b69a2
    var width = fig.width;
    var height = fig.height;
    var dx = bounds[1][0] - bounds[0][0];
    var dy = bounds[1][1] - bounds[0][1];
    var x = (bounds[0][0] + bounds[1][0]) / 2;
    var y = (bounds[0][1] + bounds[1][1]) / 2;
    var scale = Math.max(1, Math.min(8, 0.9 / Math.max(dx / width, dy / height)));
    var translate = [width / 2 - scale * x, height / 2 - scale * y];
    return {translate: translate, scale: scale}
}

mpld3.getTransformation = function(transform) {
    // https://stackoverflow.com/questions/38224875/replacing-d3-transform-in-d3-v4
    // Create a dummy g for calculation purposes only. This will never
    // be appended to the DOM and will be discarded once this function
    // returns.
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");

    // Set the transform attribute to the provided string value.
    g.setAttributeNS(null, "transform", transform);

    // consolidate the SVGTransformList containing all transformations
    // to a single SVGTransform of type SVG_TRANSFORM_MATRIX and get
    // its SVGMatrix.
    var matrix = g.transform.baseVal.consolidate().matrix;

    // Below calculations are taken and adapted from the private function
    // transform/decompose.js of D3's module d3-interpolate.
    var a = matrix.a, b = matrix.b, c = matrix.c, d = matrix.d, e = matrix.e, f = matrix.f;
    var scaleX, scaleY, skewX;
    if (scaleX = Math.sqrt(a * a + b * b)) a /= scaleX, b /= scaleX;
    if (skewX = a * c + b * d) c -= a * skewX, d -= b * skewX;
    if (scaleY = Math.sqrt(c * c + d * d)) c /= scaleY, d /= scaleY, skewX /= scaleY;
    if (a * d < b * c) a = -a, b = -b, skewX = -skewX, scaleX = -scaleX;

    var transformObj = {
        translateX: e,
        translateY: f,
        rotate: Math.atan2(b, a) * 180 / Math.PI,
        skewX: Math.atan(skewX) * 180 / Math.PI,
        scaleX: scaleX,
        scaleY: scaleY
    };

    var transformStr = '' +
        'translate(' + transformObj.translateX + ',' + transformObj.translateY + ')' +
        'rotate(' + transformObj.rotate + ')' +
        'skewX(' + transformObj.skewX + ')' +
        'scale(' + transformObj.scaleX + ',' + transformObj.scaleY + ')';

    return transformStr;
}

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
    // make sure first character is a letter, not a digit (HTML 4 rules)
    var id = chars.charAt(Math.round(Math.random() * (chars.length - 11)));
    for (var i = 1; i < N; i++)
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

mpld3.path = function() {
    return mpld3_path();
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
        var functor = function(x) {
            if (typeof x == "function") { return x; }
            return function() { return x; }
        }
        var fx = functor(x),
            fy = functor(y);
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

mpld3.multiscale = mpld3_multiscale;

function mpld3_multiscale(_){
    var args = Array.prototype.slice.call(arguments, 0);
    var N = args.length;
    function scale(x) {
        args.forEach(function(mapping){
            x = mapping(x);
        });
        return x;
    }
    scale.domain = function(x) {
        if (!arguments.length) return args[0].domain();
        args[0].domain(x);
        return scale;
    };
    scale.range = function(x) {
        if (!arguments.length) return args[N - 1].range();
        args[N - 1].range(x);
        return scale;
    };
    scale.step = function(i) {
        return args[i];
    };
    return scale;
}
