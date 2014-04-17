var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Element");

suite.addBatch({
    "Element": {
        topic: load("core/element").document(),
        "A generic plot element ": {
            topic: function(mpld3) {
                return new mpld3.PlotElement(null);
            },
            "has the expected parent": function(element) {
                assert.equal(element.parent, null);
            },
            "has the expected figure reference": function(element) {
                assert.equal(element.fig, null);
            },
            "has the expected axes reference": function(element) {
                assert.equal(element.ax, null);
            }
        },
        "A generic plot element attached to an axes": {
            topic: function(mpld3) {
                MyEl.prototype = Object.create(mpld3.PlotElement.prototype);
                MyEl.constructor = MyEl;
                MyEl.prototype.requiredProps = ["A"];
                MyEl.prototype.defaultProps = {B:1, C:4};
                function MyEl(parent, props){
                    mpld3.PlotElement.call(this, parent, props);
                }
                return new MyEl(new mpld3.Figure("fig01", {width:400,
                                                           height:300}),
                                {A:3, B:10});
            },
            "has the expected parent figure reference": function(element) {
                assert.equal(element.fig, element.parent);
            },
            "has the expected axes reference": function(element) {
                assert.equal(element.ax, null);
            },
            "has the expected properties and values": function(element) {
                assert.equal(element.props.A, 3);
                assert.equal(element.props.B, 10);
                assert.equal(element.props.C, 4);
            }
        }
    }
});

suite.export(module);
