var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.PathCollection");

suite.addBatch({
    "Path Collections": {
        topic: load("elements/path").document(),
        "A simple Path collection": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 4],
                    ylim: [0, 4]
                };
                var coll_props = {
                    paths: [[[[0, 1], [1, 2], [2, 3], [3, 2], [4, 1]],
                             ['M', 'L', 'L', 'L', 'L', 'Z']]],
                    offsets: null,
                    alphas: [0, 0.25, 0.5, 0.75, 1.0] 
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var coll = new mpld3.PathCollection(ax, coll_props);
                ax.elements.push(coll);
                fig.axes.push(ax);
                fig.draw();
                return coll;
            },
            "has the expected number of offsets.": function(coll) {
                assert.equal(coll.offsets.length, 1);
            },
            "has the expected transform.": function(coll) {
                assert.equal(coll.transformFunc([0, 0], 0), "translate(0,240)");
            },
            "has the expected path.": function(coll) {
                assert.equal(coll.pathFunc([0, 0], 0),
                             "M 0 1 L 1 2 L 2 3 L 3 2 L 4 1 Z");
            },
            "has the expected style.": function(coll) {
                assert.equal(coll.styleFunc([0, 0], 0), "stroke:#000000;stroke-width:1;stroke-opacity:0;fill:#0000FF;fill-opacity:0;");
            }
        }
    }
});

suite.export(module);
