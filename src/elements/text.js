/**********************************************************************/
/* Text Element */
mpld3.Text = mpld3_Text;
mpld3_Text.prototype = Object.create(mpld3_PlotElement.prototype);
mpld3_Text.prototype.constructor = mpld3_Text;
mpld3_Text.prototype.requiredProps = ["text", "position"];
mpld3_Text.prototype.defaultProps = {
    coordinates: "data",
    h_anchor: "start",
    v_baseline: "auto",
    v_align: null,
    m_align: null,
    linespacing: 1.2,
    rotation: 0,
    fontsize: 11,
    drawstyle: "none",
    color: "black",
    alpha: 1.0,
    bbox: null,
    zorder: 3
};

function mpld3_Text(ax, props) {
    mpld3_PlotElement.call(this, ax, props);
    this.text = this.props.text;
    this.position = this.props.position;
    this.coords = new mpld3_Coordinates(this.props.coordinates, this.ax, this.fig);
};

mpld3_Text.prototype.draw = function() {
    var target;
    if (this.ax) {
        if (this.props.coordinates == "data") {
            if (this.coords.zoomable) {
                target = this.ax.paths;
            } else {
                target = this.ax.staticPaths;
            }
        } else {
            target = this.ax.baseaxes;
        }
    } else {
        target = this.fig.figureTextGroup || this.fig.canvas;
    }

    if (this.props.bbox) {
        this.group = target.append("g")
            .attr("class", "mpld3-textgroup");
        this.bbox = this.group.append("rect")
            .attr("class", "mpld3-textbox");
        this.obj = this.group.append("text");
    } else {
        this.obj = target.append("text");
    }

    this.obj
        .attr("class", "mpld3-text")
        .attr("xml:space", "preserve")
        .style("text-anchor", this.props.h_anchor)
        .style("dominant-baseline", this.props.v_baseline)
        .style("font-size", this.props.fontsize)
        .style("fill", this.props.color)
        .style("opacity", this.props.alpha);
    this._setText();
    if (this.bbox) {
        this._applyBBoxStyle();
    }
    this.applyTransform();
};

mpld3_Text.prototype.elements = function(d) {
    return d3.select(this.group || this.obj);
};

mpld3_Text.prototype._setText = function() {
    var lines = this.text.split(/\r?\n/);
    if (lines.length === 1) {
        this.obj.text(lines[0]);
        return;
    }
    this.obj.text(null);
    var lineSpacing = this.props.linespacing;
    var offsetEm = 0;
    if (this.props.v_align === "center" || this.props.v_align === "center_baseline") {
        offsetEm = -0.5 * (lines.length - 1) * lineSpacing;
    } else if (this.props.v_align === "bottom") {
        offsetEm = -(lines.length - 1) * lineSpacing;
    }

    this.obj.append("tspan").text(lines[0])
        .attr("dy", offsetEm + "em");
    for (var i = 1; i < lines.length; i++) {
        this.obj.append("tspan").text(lines[i])
            .attr("dy", lineSpacing + "em");
    }
};

mpld3_Text.prototype.applyTransform = function() {
    var pos = this.coords.xy(this.position);
    this.obj.attr("x", pos[0]).attr("y", pos[1]);
    this._applyMultilineAlignment(this.obj.selectAll("tspan"), pos[0]);
    if (this.bbox) {
        this._updateBBox();
    }

    if (this.props.rotation) {
        (this.group || this.obj).attr("transform", "rotate(" + this.props.rotation + "," + pos + ")");
    }
};

mpld3_Text.prototype._applyMultilineAlignment = function(tspans, anchorX) {
    if (tspans.size() <= 1) {
        tspans.attr("x", anchorX);
        return;
    }

    function normalizeAlign(value, fallback) {
        if (value === "start") return "left";
        if (value === "middle") return "center";
        if (value === "end") return "right";
        if (value === "left" || value === "center" || value === "right") return value;
        return fallback;
    }

    var hAlign = normalizeAlign(this.props.h_anchor, "left");
    var mAlign = normalizeAlign(this.props.m_align, hAlign);
    var widths = [];
    var maxWidth = 0;

    tspans.each(function() {
        var width = this.getComputedTextLength();
        widths.push(width);
        if (width > maxWidth) {
            maxWidth = width;
        }
    });

    var bboxLeft = anchorX;
    if (hAlign === "center") {
        bboxLeft = anchorX - maxWidth / 2;
    } else if (hAlign === "right") {
        bboxLeft = anchorX - maxWidth;
    }

    tspans.each(function(_, i) {
        var width = widths[i];
        var x = bboxLeft;
        if (mAlign === "center") {
            x = bboxLeft + (maxWidth - width) / 2;
        } else if (mAlign === "right") {
            x = bboxLeft + (maxWidth - width);
        }
        d3.select(this)
            .attr("x", x)
            .style("text-anchor", "start");
    });
};

mpld3_Text.prototype._applyBBoxStyle = function() {
    var props = this.props.bbox;
    var edgecolor = props.edgecolor || "none";
    var facecolor = props.facecolor || "none";
    var edgewidth = props.edgewidth == null ? 0 : props.edgewidth;
    var dasharray = props.dasharray == null ? "none" : props.dasharray;

    this.bbox
        .style("fill", facecolor)
        .style("stroke", edgecolor)
        .style("stroke-width", edgewidth)
        .style("stroke-dasharray", dasharray)
        .attr("vector-effect", "non-scaling-stroke");

    if (edgecolor.slice(0, 5) != "rgba(") {
        this.bbox.style("stroke-opacity", props.alpha);
    }
    if (facecolor.slice(0, 5) != "rgba(") {
        this.bbox.style("fill-opacity", props.alpha);
    }
};

mpld3_Text.prototype._updateBBox = function() {
    var props = this.props.bbox;
    var textBox = this.obj.node().getBBox();
    var pad = props.pad == null ? 0 : props.pad;
    var scale = props.mutation_scale == null ? this.props.fontsize : props.mutation_scale;
    var aspect = props.mutation_aspect == null ? 1 : props.mutation_aspect;
    var paddingX = pad * scale;
    var paddingY = pad * scale * aspect;
    var x = textBox.x - paddingX;
    var y = textBox.y - paddingY;
    var width = textBox.width + 2 * paddingX;
    var height = textBox.height + 2 * paddingY;

    this.bbox
        .attr("x", x)
        .attr("y", y)
        .attr("width", width)
        .attr("height", height);

    var radius = 0;
    if (props.boxstyle && props.boxstyle.toLowerCase().indexOf("round") !== -1) {
        var rounding = props.rounding_size == null ? pad : props.rounding_size;
        radius = rounding * scale;
    }
    if (radius > 0) {
        this.bbox.attr("rx", radius).attr("ry", radius);
    } else {
        this.bbox.attr("rx", null).attr("ry", null);
    }
};

// TODO: (@vladh) Remove legacy zooming code.
// mpld3_Text.prototype.zoomed = function() {
//     if (this.coords.zoomable)
//         this.applyTransform();
// };
