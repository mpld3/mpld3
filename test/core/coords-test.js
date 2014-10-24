var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe('mpld3.Coordinates')

suite.addBatch({
    "Coordinates": {
	topic: load("core/figure", "core/axes", "core/coordinates").document(),
	"A Coordinates('display') object": {
	    topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300,
                    axes: [{xlim: [0, 1], ylim: [0, 1]}]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                fig.draw();
                return new mpld3.Coordinates("display", fig.axes[0]);
	    },
	    "transforms to the correct display coordinates": function(coords){
                assert.equal(coords.xy([100, 100])[0], 100);
                assert.equal(coords.xy([100, 100])[1], 100);
	    }
	},
	"A Coordinates('data') object": {
	    topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300,
                    axes: [{xlim: [-1, 1], ylim: [-1, 1]}]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                fig.draw();
                return new mpld3.Coordinates("data", fig.axes[0]);
	    },
	    "transforms to the correct display coordinates": function(coords){
                assert.equal(coords.xy([0.3, 0.4])[0], 208);
                assert.equal(Math.round(coords.xy([0.3, 0.4])[1]*1000), Math.round(72*1000));
	    }
	},
	"A Coordinates('axes') object": {
	    topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300,
                    axes: [{xlim: [-1, 1], ylim: [-1, 1]}]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                fig.draw();
                return new mpld3.Coordinates("axes", fig.axes[0]);
	    },
	    "transforms to the correct display coordinates": function(coords){
                assert.equal(coords.xy([0.3, 0.4])[0], 96);
                assert.equal(coords.xy([0.3, 0.4])[1], 144);
	    }
	},
	"A Coordinates('figure') object": {
	    topic: function(mpld3) {
                var fig_props = {
                    width: 400,
                    height: 300,
                    axes: [{xlim: [-1, 1], ylim: [-1, 1]}]
                };
                var fig = new mpld3.Figure("chart", fig_props);
                fig.draw();
                return new mpld3.Coordinates("figure", fig.axes[0]);
	    },
	    "transforms to the correct display coordinates": function(coords){
                assert.equal(coords.xy([0.3, 0.4])[0], 80);
                assert.equal(coords.xy([0.3, 0.4])[1], 150);
	    }
	}
    }
});

suite.export(module);
