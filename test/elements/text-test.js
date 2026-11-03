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

suite.addBatch({
    "Zooming text": {
        topic: load("elements/path").document(),
        "keeps data text at a fixed size while its anchor moves": function(mpld3) {
            var d3 = require("d3");
            var container = document.createElement("div");
            container.id = "zoom-chart";
            document.body.appendChild(container);
            var fig = new mpld3.Figure("zoom-chart", {
                width: 400, height: 300, plugins: [],
                axes: [{xlim: [0, 4], ylim: [0, 4], axes: [], texts: [
                    {text: "data", position: [1, 3], rotation: 30},
                    {text: "axes", position: [0.5, 0.5], coordinates: "axes"}
                ]}]
            });
            fig.draw();
            var ax = fig.axes[0];
            var texts = ax.elements.filter(function(element) { return element instanceof mpld3.Text; });
            var text = texts[0], fixedText = texts[1];
            var pos = text.coords.xy(text.position);
            var rotation = "rotate(30," + pos + ")";
            var parent = text.obj.node().parentNode;
            ax.bindZoom();
            ax.zoom.extent([[0, 0], [ax.width, ax.height]]);
            [2, 0.5, 4].forEach(function(k) {
                ax.doZoom(false, d3.zoomIdentity.translate(10, 20).scale(k), false);
                assert.equal(text.obj.attr("transform"),
                    "translate(" + pos + ")scale(" + (1 / k) + ")translate(" +
                    [-pos[0], -pos[1]] + ")" + rotation);
                assert.equal(text.obj.attr("x"), pos[0]);
                assert.equal(text.obj.attr("y"), pos[1]);
                assert.equal(text.obj.node().parentNode, parent);
                assert.equal(fixedText.obj.attr("transform"), null);
            });
            ax.doZoom(false, d3.zoomIdentity, false);
            assert.equal(text.obj.attr("transform"), rotation);
            container.parentNode.removeChild(container);
        }
    }
});

suite.export(module);
