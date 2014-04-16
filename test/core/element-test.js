var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe("mpld3.Element");

suite.addBatch({
    "Element": {
        topic: load("core/element").document(),
        "simple Element": {
            topic: function(mpld3) {
                return new mpld3.PlotElement(null);
            },
            "check element": function(element) {
                assert.equal(element.parent, null);
                assert.equal(element.fig, null);
                assert.equal(element.ax, null);
            }
        },
        "basic Element": {
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
            "check element": function(element) {
                assert.equal(element.fig, element.parent);
                assert.equal(element.ax, null);
                assert.equal(element.props.A, 3);
                assert.equal(element.props.B, 10);
                assert.equal(element.props.C, 4);
            }
        }
    }
});

suite.export(module);
