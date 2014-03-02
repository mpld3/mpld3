"""
Visualizing Random Walks
========================
This shows the use of transparent lines to visualize random walk data.
Thre is also a custom plugin defined which causes lines to be highlighted
when the mouse hovers over them.
"""
import jinja2
import json
import numpy as np
import matplotlib.pyplot as plt

import mpld3
from mpld3 import plugins, utils

class HighlightLines(plugins.PluginBase):
    """A plugin to highlight lines on hover"""

    JAVASCRIPT = """
    var LineHighlightPlugin = function(fig, prop){
       this.fig = fig;
       this.prop = mpld3.process_props(this, prop,
                                       {alpha_bg:0.3, alpha_fg:1.0},
                                       ["line_ids"]);
    };

    LineHighlightPlugin.prototype.draw = function(){
      for(var i=0; i<this.prop.line_ids.length; i++){
         var obj = mpld3.get_element(this.prop.line_ids[i]),
             alpha_fg = this.prop.alpha_fg;
             alpha_bg = this.prop.alpha_bg;
         obj.elements()
             .on("mouseover", function(d, i){
                            d3.select(this).transition().duration(50)
                                .style("stroke-opacity", alpha_fg)
                          })
             .on("mouseout", function(d, i){
                            d3.select(this).transition().duration(200)
                                .style("stroke-opacity", alpha_bg);
                          });
      }
    };

    mpld3.register_plugin("linehighlight", LineHighlightPlugin);
    """

    def __init__(self, lines):
        self.lines = lines
        self.dict_ = {"type": "linehighlight",
                      "line_ids": [utils.get_id(line) for line in lines],
                      "alpha_bg": lines[0].get_alpha(),
                      "alpha_fg": 1.0}


N_paths = 50
N_steps = 100

x = np.linspace(0, 10, 100)
y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
y = y.cumsum(1)

fig, ax = plt.subplots(subplot_kw={'xticks': [], 'yticks': []})
lines = ax.plot(x, y.T, color='blue', lw=4, alpha=0.1)
plugins.connect(fig, HighlightLines(lines))

mpld3.show()
