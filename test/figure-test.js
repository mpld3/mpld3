var vows = require("vows"),
    load = require("./load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Figure");

suite.addBatch({
    "Figure": {
        topic: load("figure").document(),
        "simple figure": {
            topic: function(mpld3) {
                var props = {
                    width: 100,
                    height: 200
                };
                return new mpld3.Figure("chart", props)
            },
            "inserts a new figure element": function(figure) {
                assert.equal(figure.figid, "chart");
                assert.equal(figure.props.width, 100);
                assert.equal(figure.props.height, 200);
            }
        }
    }
});

suite.export(module);
