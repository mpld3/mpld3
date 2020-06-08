"""

NetworkX to d3.js Force Layout
==============================

MPLD3 Plugin to convert a NetworkX graph to a force layout.
This is an example demoed `here
<http://blog.kdheepak.com/mpld3-networkx-d3js-force-layout.html>`_
You can download the plugin from the Github repo `here
<https://github.com/kdheepak/mpld3_plugins/blob/master/mpld3_plugins/plugins/networkxd3forcelayout.py>`_

BSD-Clause 3 License
Copyright (C) 2016 Dheepak Krishnamurthy
"""


import mpld3

graph = {'directed': False,
 'graph': {'name': "Zachary's Karate Club"},
 'links': [{'source': 0, 'target': 1},
  {'source': 0, 'target': 2},
  {'source': 0, 'target': 3},
  {'source': 0, 'target': 4},
  {'source': 0, 'target': 5},
  {'source': 0, 'target': 6},
  {'source': 0, 'target': 7},
  {'source': 0, 'target': 8},
  {'source': 0, 'target': 10},
  {'source': 0, 'target': 11},
  {'source': 0, 'target': 12},
  {'source': 0, 'target': 13},
  {'source': 0, 'target': 17},
  {'source': 0, 'target': 19},
  {'source': 0, 'target': 21},
  {'source': 0, 'target': 31},
  {'source': 1, 'target': 2},
  {'source': 1, 'target': 3},
  {'source': 1, 'target': 7},
  {'source': 1, 'target': 13},
  {'source': 1, 'target': 17},
  {'source': 1, 'target': 19},
  {'source': 1, 'target': 21},
  {'source': 1, 'target': 30},
  {'source': 2, 'target': 3},
  {'source': 2, 'target': 32},
  {'source': 2, 'target': 7},
  {'source': 2, 'target': 8},
  {'source': 2, 'target': 9},
  {'source': 2, 'target': 13},
  {'source': 2, 'target': 27},
  {'source': 2, 'target': 28},
  {'source': 3, 'target': 7},
  {'source': 3, 'target': 12},
  {'source': 3, 'target': 13},
  {'source': 4, 'target': 10},
  {'source': 4, 'target': 6},
  {'source': 5, 'target': 16},
  {'source': 5, 'target': 10},
  {'source': 5, 'target': 6},
  {'source': 6, 'target': 16},
  {'source': 8, 'target': 32},
  {'source': 8, 'target': 30},
  {'source': 8, 'target': 33},
  {'source': 9, 'target': 33},
  {'source': 13, 'target': 33},
  {'source': 14, 'target': 32},
  {'source': 14, 'target': 33},
  {'source': 15, 'target': 32},
  {'source': 15, 'target': 33},
  {'source': 18, 'target': 32},
  {'source': 18, 'target': 33},
  {'source': 19, 'target': 33},
  {'source': 20, 'target': 32},
  {'source': 20, 'target': 33},
  {'source': 22, 'target': 32},
  {'source': 22, 'target': 33},
  {'source': 23, 'target': 32},
  {'source': 23, 'target': 25},
  {'source': 23, 'target': 27},
  {'source': 23, 'target': 29},
  {'source': 23, 'target': 33},
  {'source': 24, 'target': 25},
  {'source': 24, 'target': 27},
  {'source': 24, 'target': 31},
  {'source': 25, 'target': 31},
  {'source': 26, 'target': 33},
  {'source': 26, 'target': 29},
  {'source': 27, 'target': 33},
  {'source': 28, 'target': 33},
  {'source': 28, 'target': 31},
  {'source': 29, 'target': 32},
  {'source': 29, 'target': 33},
  {'source': 30, 'target': 33},
  {'source': 30, 'target': 32},
  {'source': 31, 'target': 33},
  {'source': 31, 'target': 32},
  {'source': 32, 'target': 33}],
 'multigraph': False,
 'nodes': [{'club': 'Mr. Hi', 'color': 'purple', 'id': 0, 'size': 16},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 1, 'size': 9},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 2, 'size': 10},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 3, 'size': 6},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 4, 'size': 3},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 5, 'size': 4},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 6, 'size': 4},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 7, 'size': 4},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 8, 'size': 5},
  {'club': 'Officer', 'color': 'orange', 'id': 9, 'size': 2},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 10, 'size': 3},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 11, 'size': 1},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 12, 'size': 2},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 13, 'size': 5},
  {'club': 'Officer', 'color': 'orange', 'id': 14, 'size': 2},
  {'club': 'Officer', 'color': 'orange', 'id': 15, 'size': 2},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 16, 'size': 2},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 17, 'size': 2},
  {'club': 'Officer', 'color': 'orange', 'id': 18, 'size': 2},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 19, 'size': 3},
  {'club': 'Officer', 'color': 'orange', 'id': 20, 'size': 2},
  {'club': 'Mr. Hi', 'color': 'purple', 'id': 21, 'size': 2},
  {'club': 'Officer', 'color': 'orange', 'id': 22, 'size': 2},
  {'club': 'Officer', 'color': 'orange', 'id': 23, 'size': 5},
  {'club': 'Officer', 'color': 'orange', 'id': 24, 'size': 3},
  {'club': 'Officer', 'color': 'orange', 'id': 25, 'size': 3},
  {'club': 'Officer', 'color': 'orange', 'id': 26, 'size': 2},
  {'club': 'Officer', 'color': 'orange', 'id': 27, 'size': 4},
  {'club': 'Officer', 'color': 'orange', 'id': 28, 'size': 3},
  {'club': 'Officer', 'color': 'orange', 'id': 29, 'size': 4},
  {'club': 'Officer', 'color': 'orange', 'id': 30, 'size': 4},
  {'club': 'Officer', 'color': 'orange', 'id': 31, 'size': 6},
  {'club': 'Officer', 'color': 'orange', 'id': 32, 'size': 12},
  {'club': 'Officer', 'color': 'orange', 'id': 33, 'size': 17}]}

class NetworkXD3ForceLayout(mpld3.plugins.PluginBase):
    """A NetworkX to D3 Force Layout Plugin"""

    JAVASCRIPT = """
    mpld3.register_plugin("networkxd3forcelayout", NetworkXD3ForceLayoutPlugin);
    NetworkXD3ForceLayoutPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    NetworkXD3ForceLayoutPlugin.prototype.constructor = NetworkXD3ForceLayoutPlugin;
    NetworkXD3ForceLayoutPlugin.prototype.requiredProps = ["graph",
                                                                "ax_id",];
    NetworkXD3ForceLayoutPlugin.prototype.defaultProps = { coordinates: "data",
                                                               gravity: 1,
                                                               charge: -30,
                                                               link_strength: 1,
                                                               friction: 0.9,
                                                               link_distance: 20,
                                                               maximum_stroke_width: 2,
                                                               minimum_stroke_width: 1,
                                                               nominal_stroke_width: 1,
                                                               maximum_radius: 10,
                                                               minimum_radius: 1,
                                                               nominal_radius: 5,
                                                            };
    function NetworkXD3ForceLayoutPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    var color = d3.scaleOrdinal(d3.schemeCategory10);
    NetworkXD3ForceLayoutPlugin.prototype.zoomScaleProp = function (nominal_prop, minimum_prop, maximum_prop) {
        var zoom = this.ax.zoom;
        scalerFunction = function() {
            var prop = nominal_prop;
            if (nominal_prop*zoom.scale()>maximum_prop) prop = maximum_prop/zoom.scale();
            if (nominal_prop*zoom.scale()<minimum_prop) prop = minimum_prop/zoom.scale();
            return prop
        }
        return scalerFunction;
    }
    NetworkXD3ForceLayoutPlugin.prototype.setupDefaults = function () {
        this.zoomScaleStroke = this.zoomScaleProp(this.props.nominal_stroke_width,
                                                  this.props.minimum_stroke_width,
                                                  this.props.maximum_stroke_width)
        this.zoomScaleRadius = this.zoomScaleProp(this.props.nominal_radius,
                                                  this.props.minimum_radius,
                                                  this.props.maximum_radius)
    }
    NetworkXD3ForceLayoutPlugin.prototype.zoomed = function() {
        this.tick()
    }
    NetworkXD3ForceLayoutPlugin.prototype.draw = function(){
        plugin = this
        DEFAULT_NODE_SIZE = this.props.nominal_radius;
        var height = this.fig.height
        var width = this.fig.width
        var graph = this.props.graph
        var gravity = this.props.gravity.toFixed()
        var charge = this.props.charge.toFixed()
        var link_distance = this.props.link_distance.toFixed()
        var link_strength = this.props.link_strength.toFixed()
        var friction = this.props.friction.toFixed()
        this.ax = mpld3.get_element(this.props.ax_id, this.fig)
        var ax = this.ax;
        this.ax.elements.push(this)
        ax_obj = this.ax;
        var width = d3.max(ax.x.range()) - d3.min(ax.x.range()),
            height = d3.max(ax.y.range()) - d3.min(ax.y.range());
        var color = d3.scaleOrdinal(d3.schemeCategory10);
        this.xScale = d3.scaleLinear().domain([0, 1]).range([0, width]) // ax.x;
        this.yScale = d3.scaleLinear().domain([0, 1]).range([height, 0]) // ax.y;
        this.force = d3.forceSimulation();
        this.svg = this.ax.axes.append("g");
        for(var i = 0; i < graph.nodes.length; i++){
            var node = graph.nodes[i];
            if (node.hasOwnProperty('x')) {
                node.x = this.ax.x(node.x);
            }
            if (node.hasOwnProperty('y')) {
                node.y = this.ax.y(node.y);
            }
        }
        this.force
            .force("link",
                d3.forceLink()
                    .id(function(d) { return d.index })
                    .strength(link_strength)
                    .distance(link_distance)
            )
            .force("collide", d3.forceCollide(function(d){return d.r + 8 }).iterations(16))
            .force("charge", d3.forceManyBody().strength(charge))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("y", d3.forceY(0))
            .force("x", d3.forceX(0));
        this.force.nodes(graph.nodes);
        this.force.force("link").links(graph.links);
        this.link = this.svg.selectAll(".link")
            .data(graph.links)
          .enter().append("line")
            .attr("class", "link")
            .attr("stroke", "black")
            .style("stroke-width", function (d) { return Math.sqrt(d.value); });
        this.node = this.svg.selectAll(".node")
            .data(graph.nodes)
          .enter().append("circle")
            .attr("class", "node")
            .attr("r", function(d) {return d.size === undefined ? DEFAULT_NODE_SIZE : d.size ;})
            .style("fill", function (d) { return color(d); });
        this.node.append("title")
            .text(function (d) { return d.name; });
        this.force.on("tick", this.tick.bind(this));
        this.setupDefaults()
    };
    NetworkXD3ForceLayoutPlugin.prototype.tick = function() {
        this.link.attr("x1", function (d) { return this.ax.x(this.xScale.invert(d.source.x)); }.bind(this))
                 .attr("y1", function (d) { return this.ax.y(this.yScale.invert(d.source.y)); }.bind(this))
                 .attr("x2", function (d) { return this.ax.x(this.xScale.invert(d.target.x)); }.bind(this))
                 .attr("y2", function (d) { return this.ax.y(this.yScale.invert(d.target.y)); }.bind(this));
        this.node.attr("transform", function (d) {
            return "translate(" + this.ax.x(this.xScale.invert(d.x)) + "," + this.ax.y(this.yScale.invert(d.y)) + ")";
            }.bind(this)
        );
    }
    """

    def __init__(self, graph, ax,
                 gravity=1,
                 link_distance=20,
                 charge=-30,
                 node_size=5,
                 link_strength=1,
                 friction=0.9):

        self.dict_ = {"type": "networkxd3forcelayout",
                      "graph": graph,
                      "ax_id": mpld3.utils.get_id(ax),
                      "gravity": gravity,
                      "charge": charge,
                      "friction": friction,
                      "link_distance": link_distance,
                      "link_strength": link_strength,
                      "nominal_radius": node_size}

import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 1, figsize=(10, 10))
ax = axs

mpld3.plugins.connect(fig, NetworkXD3ForceLayout(graph,
                                                 ax,
                                                 gravity=.5,
                                                 link_distance=20,
                                                 charge=-600,
                                                 friction=1
                                                )
                     )

mpld3.show()
