var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Markers");

suite.addBatch({
    "Markers": {
        topic: load("elements/markers").document(),
        "A simple set of circle markers": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300,
                };
                var ax_props = {
                    xlim: [0, 1],
                    ylim: [2, 3],
                };
                var marker_props = {
                    markername: "circle",
                    data: [[0, 2], [1, 3]]
                };
                var fig = new mpld3.Figure("fig01", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var markers = new mpld3.Markers(ax, marker_props);
                ax.elements.push(markers);
                fig.axes.push(ax);
                fig.draw();
                return markers;
            },
            "has the expected marker path": function(markers) {
                console.log(markers.marker);
                let expected = "M3.385137501286538,0A3.385137501286538,3.385137501286538,0,1,1,-3.385137501286538,0A3.385137501286538,3.385137501286538,0,1,1,3.385137501286538,0";
                console.log(expected);
                assert.equal(markers.marker, expected);
            },
            "has the expected offsets": function(markers) {
                assert.equal(markers.offsets[0][0], 0);
                assert.equal(markers.offsets[0][1], 2);
                assert.equal(markers.offsets[1][0], 1);
                assert.equal(markers.offsets[1][1], 3);
            }
        },
        "A set of markers with custom paths": {
            topic: function(mpld3) {
                var fig_props = {
                    width: 100,
                    height: 200
                };
                var ax_props = {
                    xlim: [0, 1],
                    ylim: [2, 3]
                };
                var marker_props = {
                    markerpath: [[[0, 0], [1, 0], [1, 1], [0, 1]],
                                 ["M", "L", "L", "L", "Z"]],
                    data: [[0, 1], [2, 3]]
                };
                var fig = new mpld3.Figure("fig01", fig_props);
                var ax = new mpld3.Axes(fig, ax_props);
                var markers = new mpld3.Markers(ax, marker_props);
                ax.elements.push(markers);
                fig.axes.push(ax);
                fig.draw();
                return markers;
            },
            "has the expected SVG output": function(markers) {
                assert.equal(markers.marker, "M 0 0 L 1 0 L 1 1 L 0 1 Z");
            },
            "has the expected offsets": function(markers) {
                assert.equal(markers.offsets[0][0], 0);
                assert.equal(markers.offsets[0][1], 1);
                assert.equal(markers.offsets[1][0], 2);
                assert.equal(markers.offsets[1][1], 3);
            }
        }
    }
});


suite.export(module);
