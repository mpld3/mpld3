var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Figure");

suite.addBatch({
    "Figure": {
        topic: load("core/figure").document(),
        "A simple figure": {
            topic: function(mpld3) {
                var props = {
                    width: 400,
                    height: 300,
                    plugins: []
                };
                var figure = new mpld3.Figure("chart", props);
                figure.draw();
                return figure;
            },
            "has the expected id": function(figure){
                assert.equal(figure.figid, "chart");
            },
            "has the expected width and height": function(figure){
                assert.equal(figure.props.width, 400);
                assert.equal(figure.props.height, 300);
            }
        }
    }
});

suite.export(module);
