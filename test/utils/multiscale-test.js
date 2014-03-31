var vows = require("vows"),
    d3 = require("d3"),
    load = require("../load"),
    assert = require("assert");

var suite = vows.describe('mpld3.path')

suite.addBatch({
    "multiscale": {
	topic: load("utils/util").document(),
	"simple multiscale": {
	    topic: function(mpld3) {
		return mpld3.multiscale(d3.scale.linear()
                                          .domain([0, 1])
                                          .range([10, 20]),
                                        d3.scale.linear()
                                          .domain([10, 20])
                                          .range([100, 200]));
	    },
	    "Create a basic multiscale": function(m){
		assert.deepEqual(m.domain(), [0, 1]);
		assert.deepEqual(m.range(), [100, 200]);
		assert.equal(m(0.5), 150);
	    }
	},
	"modifying multiscale": {
	    topic: function(mpld3) {
		var scale1 = d3.scale.linear()
                                     .domain([0, 1])
                                     .range([10, 20]);
		var scale2 = d3.scale.linear()
                                     .domain([10, 20])
                                     .range([100, 200]);
		return [scale1, scale2, mpld3.multiscale(scale1, scale2)];
	    },
	    "Create a basic multiscale": function(tup){
		var s1 = tup[0];
		var s2 = tup[1];
		var m = tup[2];
		assert.deepEqual(m.domain(), s1.domain());
		assert.deepEqual(m.range(), s2.range());

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
		
