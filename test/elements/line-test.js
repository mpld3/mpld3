var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Line");

suite.addBatch({
    "Line": {
        topic: load("elements/line").document(),
        "A simple Line": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 5],
                    ylim: [0, 5]
                };
                var line_props = {
                    data: [[0, 0], [1, 2], [4, 5], [5, 2]]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var line = new mpld3.Line(ax, line_props);
                ax.elements.push(line);
                fig.axes.push(ax);
                fig.draw();
                return line;
            },
            "returns the expected SVG path": function(line) {
		assert.equal(line.datafunc(line.data, line.pathcodes),
                             "M0,240L64,144L256,0L320,144")
            }
        },
        "Line with NaNs": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 5],
                    ylim: [0, 5]
                };
                var line_props = {
                    data: [[0, 0], [1, 2], [3, NaN], [4, 5], [5, 2]]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var line = new mpld3.Line(ax, line_props);
                ax.elements.push(line);
                fig.axes.push(ax);
                fig.draw();
                return line;
            },
            "returns the expected SVG path": function(line) {
		assert.equal(line.datafunc(line.data, line.pathcodes),
                             "M0,240L64,144M256,0L320,144")
            }
        },
        "Line with Infs": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 5],
                    ylim: [0, 5]
                };
                var line_props = {
                    data: [[0, 0], [1, 2], [3, Infinity], [4, 5], [5, 2]]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var line = new mpld3.Line(ax, line_props);
                ax.elements.push(line);
                fig.axes.push(ax);
                fig.draw();
                return line;
            },
            "returns the expected SVG path": function(line) {
		assert.equal(line.datafunc(line.data, line.pathcodes),
                             "M0,240L64,144M256,0L320,144")
            }
        }
    }
});

suite.export(module);
