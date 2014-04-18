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
                    xlim: [0, 1],
                    ylim: [2, 3]
                };
                var line_props = {
                    data: [[0, 2], [1, 3], [2, 4]]
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
                             "M0,240L320,0L640,-240")
            }
        }
    }
});

suite.export(module);
