var vows = require("vows"),
    d3 = require("d3"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe('mpld3.path')

suite.addBatch({
    "multiscale": {
	topic: load("utils/util").document(),
	"A multiscale object": {
	    topic: function(mpld3) {
		return mpld3.multiscale(d3.scaleLinear()
                                          .domain([0, 1])
                                          .range([10, 20]),
                                        d3.scaleLinear()
                                          .domain([10, 20])
                                          .range([100, 200]));
	    },
	    "has the expected domain": function(m){
		assert.deepEqual(m.domain(), [0, 1]);
	    },
	    "has the expected range": function(m){
		assert.deepEqual(m.range(), [100, 200]);
	    },
	    "converts from domain to range as expected": function(m){
		assert.equal(m(0.5), 150);
	    }
	},
	"A modified multiscale object": {
	    topic: function(mpld3) {
		var scale1 = d3.scaleLinear()
                                     .domain([0, 1])
                                     .range([10, 20]);
		var scale2 = d3.scaleLinear()
                                     .domain([10, 20])
                                     .range([100, 200]);
		return [scale1, scale2, mpld3.multiscale(scale1, scale2)];
	    },
	    "has the expected domain": function(tup){
		var s1 = tup[0], s2 = tup[1], m = tup[2];
		assert.deepEqual(m.domain(), s1.domain());
	    },
	    "has the expected range": function(tup){
		var s1 = tup[0], s2 = tup[1], m = tup[2];
		assert.deepEqual(m.range(), s2.range());
	    },
	    "correctly behaves when domain/range are modified": function(tup){
		var s1 = tup[0], s2 = tup[1], m = tup[2];
		// modify domain and range
		m.domain([-1, 1]);
		assert.deepEqual(m.domain(), s1.domain());
		m.range([8, 16]);
		assert.deepEqual(m.range(), s2.range());
		
		// check the new multiscale mapping
		assert.deepEqual(m(3.14), s2(s1(3.14)));
	    }
	}
    }
});

suite.export(module);
