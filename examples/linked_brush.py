"""
MultiAxes Plot
==============
This example shows how to create a multi-axis plot with tied zoom.

It uses the iris dataset from scikit-learn.
"""
import jinja2

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

import mpld3
from mpld3 import plugins, utils


class LinkedBrush(plugins.PluginBase):
    JAVASCRIPT = r"""
    var LinkedBrushPlugin = function(fig, prop){
      window.fig = fig;
      this.fig = fig;
      this.prop = mpld3.process_props(this, prop, {}, ["id"]);
    }

    LinkedBrushPlugin.prototype.draw = function(){
      var obj = mpld3.get_element(this.prop.id);

      mpld3.insert_css("#" + this.fig.figid + " rect.extent",
                       {"fill": "#000",
                        "fill-opacity": .125,
                        "stroke": "#fff"});

      mpld3.insert_css("#" + this.fig.figid + " .mpld3-hidden",
                       {"stroke": "#ccc !important",
                        "fill": "#ccc !important"});

      function getDataElements(ax, data){
        for(var i=0; i< ax.elements.length; i++){
          if("elements" in ax.elements[i]
             && ax.elements[i].prop.data === data){
            return ax.elements[i];
          }
        } 
        return d3.select(null);
      }

      var brush = d3.svg.brush()
                      .on("brushstart", brushstart)
                      .on("brush", brushmove.bind(this.fig))
                      .on("brushend", brushend.bind(this.fig));

      this.fig.axes.forEach(
          function(ax){
             getDataElements(ax, obj.prop.data).elements()
                 .classed("mpld3-brushable", true);
             brush.x(ax.x)
                  .y(ax.y);
             ax.axes.call(brush);
          }
      );

      var brushAxes;
      var brushAxObj;
      var brushData;
      var fig = this.fig;

      function brushstart(){
        if(brushAxes != this){
          d3.select(brushAxes).call(brush.clear());
          brushAxes = this;
          brushAxObj = fig.axes.filter(function(ax)
                                     {return ax.axes[0][0] === brushAxes;})[0];
          brushData = getDataElements(brushAxObj, obj.prop.data);
          brush.x(brushAxObj.x).y(brushAxObj.y);
        }
      }

      function brushmove(){
        var e = brush.extent();
        this.canvas.selectAll(".mpld3-brushable")
                        .classed("mpld3-hidden",
                           function(d) {
                               return e[0][0] > d[brushData.prop.xindex] ||
                                      e[1][0] < d[brushData.prop.xindex] ||
                                      e[0][1] > d[brushData.prop.yindex] ||
                                      e[1][1] < d[brushData.prop.yindex];
                            });
      }

      function brushend(p){
        if (brush.empty()){
            this.canvas.selectAll(".mpld3-hidden")
                    .classed("mpld3-hidden", false);
        }
      }
    }

    mpld3.Toolbar.prototype.buttonDict["brush"] = mpld3.ButtonFactory({
      icon: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\nWXMAAEQkAABEJAFAZ8RUAAAAB3RJTUUH3gMCEiQKB9YaAgAAAWtJREFUOMuN0r1qVVEQhuFn700k\nnfEvBq0iNiIiOKXgH4KCaBeIhWARK/EibLwFCwVLjyAWaQzRGG9grC3URkHUBKKgRuWohWvL5pjj\nyTSLxcz7rZlZHyMiItqzFxGTEVF18/UoODNFxDIO4x12dkXqTcBPsCUzD+AK3ndFqhHwEsYz82gn\nN4dbmMRK9R/4KY7jAvbiWmYeHBT5Z4QCP8J1rGAeN3GvU3Mbl/Gq3qCDcxjLzOV+v78fq/iFIxFx\nPyJ2lNJpfBy2g59YzMyzEbEVLzGBJjOriLiBq5gaJrCIU3hcRCbwAtuwjm/Yg/V6I9NgDA1OR8RC\nZq6Vcd7iUwtn5h8fdMBdETGPE+Xe4ExELDRNs4bX2NfCUHe+7UExyfkCP8MhzOA7PuAkvrbwXyNF\nxF3MDqxiqlhXC7SPdaOKiN14g0u4g3H0MvOiTUSNY3iemb0ywmfMdfYyUmAJ2yPiBx6Wr/oy2Oqw\n+A1SupBzAOuE/AAAAABJRU5ErkJggg==\n"
    });

    mpld3.register_plugin("linkedbrush", LinkedBrushPlugin);    
    """

    def __init__(self, points):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedbrush",
                      "clear_toolbar": False,
                      "id": utils.get_id(points, suffix),
                      "buttons":"brush"}


data = load_iris()
X = data.data
y = data.target

# dither the data for clearer plotting
X += 0.1 * np.random.random(X.shape)

fig, ax = plt.subplots(4, 4, sharex="col", sharey="row", figsize=(8, 8))
fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95,
                    hspace=0.1, wspace=0.1)

for i in range(4):
    for j in range(4):
        points = ax[3 - i, j].scatter(X[:, j], X[:, i],
                                      c=y, s=40, alpha=0.6)

# remove tick labels
for axi in ax.flat:
    for axis in [axi.xaxis, axi.yaxis]:
        axis.set_major_formatter(plt.NullFormatter())

plugins.connect(fig, LinkedBrush(ax[0, 2].collections[0]))

mpld3.show()
