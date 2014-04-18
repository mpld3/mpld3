var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Axes");

suite.addBatch({
    "Axes": {
        topic: load("core/figure", "core/axes").document(),
        "A simple axes": {
            topic: function(mpld3) {
                var ax_props = {
                    xlim: [0, 1],
                    ylim: [0, 1],
                    bbox: [0.1, 0.1, 0.8, 0.8],
                    axes: []
                };
                var fig_props = {
                    width: 400,
                    height: 300,
                    plugins: [],
                    axes: [ax_props]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                fig.draw();
                return fig.axes[0];
            },
            "has the expected axnum": function(ax) {
                assert.equal(ax.axnum, 0);
            },
            "has the expected dimensions": function(ax) {
                assert.equal(ax.width, 400 * 0.8);
                assert.equal(ax.height, 300 * 0.8);
            }
        }
    }
});

suite.export(module);
