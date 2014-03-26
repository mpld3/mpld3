var vows = require("vows"),
    load = require("./load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Line");

suite.addBatch({
    "Line": {
        topic: load("line").document(),
        "simple Line": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 100,
                    height: 200
                };
                var ax_props = {
                    xlim: [0, 1],
                    ylim: [2, 3]

                }
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                return new mpld3.Line(ax, {
                    data: {
                        x: [0, 1],
                        y: [2, 3]
                    }
                });
            },
            "draw line": function(line) {
                xdom = line.ax.x.domain()
                assert.equal(xdom[0], 0)
                assert.equal(xdom[1], 1)
                ydom = line.ax.y.domain()
                assert.equal(ydom[0], 2)
                assert.equal(ydom[1], 3)
            }
        }
    }
});

suite.export(module);
