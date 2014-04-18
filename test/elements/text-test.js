var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Text");

suite.addBatch({
    "Text": {
        topic: load("elements/path").document(),
        "A simple Text object": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 4],
                    ylim: [0, 4]
                };
                var text_props = {
                    text: "hello world",
                    position: [1, 3]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var text = new mpld3.Text(ax, text_props);
                ax.elements.push(text);
                fig.axes.push(ax);
                fig.draw();
                return text;
            },
            "contains the expected text": function(text) {
                assert.equal(text.text, "hello world");
            },
            "has the expected coordinate transform": function(text) {
                assert.equal(text.props.coordinates, "data");
            },
            "has the expected position": function(text) {
                assert.equal(text.position[0], 1);
                assert.equal(text.position[1], 3);
            }
        }
    }
});

suite.export(module);
