var vows = require("vows"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe('mpld3.path')

suite.addBatch({
    "path": {
	topic: load("utils/util").document(),
	"A simple straight line path": {
	    topic: function(mpld3) {
		var data = [[0, 1], [1, 2], [2, 3]];
		return mpld3.path().call(data);
	    },
	    "returns the correct SVG codes": function(path){
		assert.equal(path, "M 0 1 L 1 2 L 2 3");
	    }
	},
	"A simple quadratic path": {
	    topic: function(mpld3) {
		var data = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]];
		var pathcodes = ['M', 'Q', 'Q']
		return mpld3.path().call(data, pathcodes);
	    },
	    "returns the correct SVG codes": function(path){
		assert.equal(path, "M 0 1 Q 1 2 2 3 Q 3 4 4 5");
	    }
	},
	"A simple closed path": {
	    topic: function(mpld3) {
		var data = [[0, 0], [1, 0], [0, 1]];
		var pathcodes = ['M', 'L', 'L', 'Z'];
		return mpld3.path().call(data, pathcodes);
	    },
	    "returns the correct SVG codes": function(path){
		assert.equal(path, "M 0 0 L 1 0 L 0 1 Z");
	    }
	}
    }
});

suite.export(module);
