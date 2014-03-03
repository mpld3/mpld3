"""
Linked Brushing Example
=======================
This example shows a prototype of a linked brush plot, using the iris dataset
from scikit-learn.  Eventually, this plugin will be made a part of the mpld3
javascript source.  For now, this should be considered a proof-of-concept.

Click the paintbrush button at the bottom left to enable and disable the
brushing behavior.  The standard zoom and home buttons are available as well.
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

      var brush_plug = this;

      mpld3.Toolbar.prototype.buttonDict["brush"] = mpld3.ButtonFactory({
        onClick: this.onClick.bind(this),
        draw: function(){
            mpld3.BaseButton.prototype.draw.apply(this);
            var enable_zoom = brush_plug.fig.enable_zoom.bind(brush_plug.fig);
            var disable_brush = brush_plug.disable.bind(brush_plug);
            brush_plug.fig.enable_zoom = function(){
                   disable_brush();
                   fig.toolbar.toolbar.selectAll(".mpld3-brushbutton")
                       .classed({pressed: false,
                                 active: false});
                   enable_zoom();
            };
            this.onClick();  // enable the button
        },
        icon: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\nWXMAAEQkAABEJAFAZ8RUAAAAB3RJTUUH3gMCEiQKB9YaAgAAAWtJREFUOMuN0r1qVVEQhuFn700k\nnfEvBq0iNiIiOKXgH4KCaBeIhWARK/EibLwFCwVLjyAWaQzRGG9grC3URkHUBKKgRuWohWvL5pjj\nyTSLxcz7rZlZHyMiItqzFxGTEVF18/UoODNFxDIO4x12dkXqTcBPsCUzD+AK3ndFqhHwEsYz82gn\nN4dbmMRK9R/4KY7jAvbiWmYeHBT5Z4QCP8J1rGAeN3GvU3Mbl/Gq3qCDcxjLzOV+v78fq/iFIxFx\nPyJ2lNJpfBy2g59YzMyzEbEVLzGBJjOriLiBq5gaJrCIU3hcRCbwAtuwjm/Yg/V6I9NgDA1OR8RC\nZq6Vcd7iUwtn5h8fdMBdETGPE+Xe4ExELDRNs4bX2NfCUHe+7UExyfkCP8MhzOA7PuAkvrbwXyNF\nxF3MDqxiqlhXC7SPdaOKiN14g0u4g3H0MvOiTUSNY3iemb0ywmfMdfYyUmAJ2yPiBx6Wr/oy2Oqw\n+A1SupBzAOuE/AAAAABJRU5ErkJggg==\n",
       });
    }

    LinkedBrushPlugin.prototype.onClick = function(){
      if(this.enabled){
        this.disable();
      }else{
        this.enable();
        this.fig.disable_zoom();
        fig.toolbar.toolbar.selectAll(".mpld3-movebutton")
                   .classed({pressed: false,
                             active: false});
      }
      this.fig.toolbar.toolbar.selectAll(".mpld3-brushbutton")
                .classed({pressed: this.enabled,
                          active: !this.enabled});
    }

    LinkedBrushPlugin.prototype.draw = function(){
      var obj = mpld3.get_element(this.prop.id);
      var fig = this.fig;
      var dataKey = ("offsets" in obj.prop) ? "offsets" : "data";

      mpld3.insert_css("#" + fig.figid + " rect.extent",
                       {"fill": "#000",
                        "fill-opacity": .125,
                        "stroke": "#fff"});

      mpld3.insert_css("#" + fig.figid + " path.mpld3-hidden",
                       {"stroke": "#ccc !important",
                        "fill": "#ccc !important"});

      var dataClass = "mpld3data-" + obj.prop[dataKey];

      var brush = d3.svg.brush()
                      .on("brushstart", brushstart)
                      .on("brush", brushmove)
                      .on("brushend", brushend);

      // Label all data points for access below
      fig.axes.forEach(function(ax){
         ax.elements.forEach(function(el){
            if(el.prop[dataKey] === obj.prop[dataKey]){
               el.group.classed(dataClass, true);
            }
         });
         brush.x(ax.x).y(ax.y);
         //ax.axes.call(brush);
      });


      // For fast brushing, precompute a list of selection properties
      // properties to apply to the selction.
      var data_map = [];
      var dataToBrush = fig.canvas.selectAll("." + dataClass)
                           .each(function(){
                              for(var i=0; i<fig.axes.length; i++){
                                var ax = fig.axes[i];
                                for(var j=0; j<ax.elements.length; j++){
                                  var el = ax.elements[j];
                                  if("group" in el && el.group[0][0] === this){
                                    data_map.push({i_ax: i,
                                                   ix: el.prop.xindex,
                                                   iy: el.prop.yindex});
                                    return;
                                  }
                                }
                              }
                            });

      dataToBrush.data(data_map)
                 .call(brush);

      var currentData;

      function brushstart(d){
        if(currentData != this){
          d3.select(currentData).call(brush.clear());
          currentData = this;
          brush.x(fig.axes[d.i_ax].x)
               .y(fig.axes[d.i_ax].y);
        }
      }

      function brushmove(d){
        var e = brush.extent();
        dataToBrush.selectAll("path")
                   .classed("mpld3-hidden",
                       function(p) {
                           return e[0][0] > p[d.ix] ||  e[1][0] < p[d.ix] ||
                                  e[0][1] > p[d.iy] || e[1][1] < p[d.iy];
                       });
      }

      function brushend(d){
        if (brush.empty()){
            dataToBrush.selectAll("path")
                       .classed("mpld3-hidden", false);
        }
      }

      function brushend_clear(){
        d3.select(this).call(brush.clear());
      }

      this.enable = function(){
        brush.on("brushstart", brushstart)
             .on("brush", brushmove)
             .on("brushend", brushend);
        this.fig.canvas.selectAll("rect.background")
              .style("cursor", "crosshair");
        this.fig.canvas.selectAll("rect.extent, rect.resize")
              .style("display", null);
        this.enabled = true;
      }

      this.disable = function(){
        brush.on("brushstart", null)
             .on("brush", null)
             .on("brushend", brushend_clear)
             .clear();
        this.fig.canvas.selectAll("rect.background")
              .style("cursor", null);
        this.fig.canvas.selectAll("rect.extent, rect.resize")
              .style("display", "none");
        this.enabled = false;
      }

      this.disable();
    }

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
                      "buttons": "brush"}


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
