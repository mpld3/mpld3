var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Text");

suite.addBatch({
    "Image": {
        topic: load("elements/path").document(),
        "A simple Image": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 4],
                    ylim: [0, 4]
                };
                var img_props = {
                    data: "NdxDRpYZ6D9YTVL09/fjP8zDz+GgeOM/nlErkxBJ6D8=",
                    extent: [0, 0, 1, 2],
                    alpha: 0.5
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var img = new mpld3.Image(ax, img_props);
                ax.elements.push(img);
                fig.axes.push(ax);
                fig.draw();
                return img;
            },
            "contains the expected data": function(img) {
                assert.equal(img.props.data,
                             "NdxDRpYZ6D9YTVL09/fjP8zDz+GgeOM/nlErkxBJ6D8=");
            },
            "has the expected extent": function(img) {
                assert.equal(img.props.extent[0], 0);
                assert.equal(img.props.extent[1], 0);
                assert.equal(img.props.extent[2], 1);
                assert.equal(img.props.extent[3], 2);
            },
            "has the expected transparency": function(img) {
                assert.equal(img.props.alpha, 0.5);
            }
        }
    }
});

suite.export(module);
