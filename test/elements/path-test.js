var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Line");

suite.addBatch({
    "Path": {
        topic: load("elements/path").document(),
        "A simple Path": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300
                };
                var ax_props = {
                    xlim: [0, 4],
                    ylim: [0, 4]
                };
                var path_props = {
                    data: [[0, 1], [1, 2], [2, 3], [3, 2], [4, 1]],
                    pathcodes: ['M', 'L', 'L', 'L', 'L', 'Z']
                };
                var fig = new mpld3.Figure("chart", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var path = new mpld3.Path(ax, path_props);
                ax.elements.push(path);
                fig.axes.push(ax);
                fig.draw();
                return path;
            },
            "has the expected SVG path.": function(path) {
                assert.equal(path.datafunc(path.data, path.pathcodes),
                             "M 0 180 L 80 120 L 160 60 L 240 120 L 320 180 Z");
            }
        }
    }
});

suite.export(module);
