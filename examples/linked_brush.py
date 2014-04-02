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
    mpld3.register_plugin("linkedbrush", LinkedBrushPlugin);
    LinkedBrushPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LinkedBrushPlugin.prototype.constructor = LinkedBrushPlugin;
    LinkedBrushPlugin.prototype.requiredProps = ["id"];
    LinkedBrushPlugin.prototype.defaultProps = {};

    function LinkedBrushPlugin(fig, props){
      mpld3.Plugin.call(this, fig, props);

      var BrushButton = mpld3.ButtonFactory({
          buttonID: "linkedbrush",
          sticky: true,
          actions: ["drag"],
          onActivate: this.activate.bind(this),
          onDeactivate: this.deactivate.bind(this),
          onDraw: this.deactivate.bind(this),
	  icon: function(){return mpld3.icons["brush"];},
      });
      this.fig.buttons.push(BrushButton);
      this.extentClass = "linkedbrush";
    }

    LinkedBrushPlugin.prototype.activate = function(){
         if(this.enable) this.enable();
    };
    LinkedBrushPlugin.prototype.deactivate = function(){
         if(this.disable) this.disable();
    };

    LinkedBrushPlugin.prototype.draw = function(){
      var obj = mpld3.get_element(this.props.id);
      var fig = this.fig;
      var dataKey = ("offsets" in obj.props) ? "offsets" : "data";

      mpld3.insert_css("#" + fig.figid + " rect.extent." + this.extentClass,
                       {"fill": "#000",
                        "fill-opacity": .125,
                        "stroke": "#fff"});

      mpld3.insert_css("#" + fig.figid + " path.mpld3-hidden",
                       {"stroke": "#ccc !important",
                        "fill": "#ccc !important"});

      var dataClass = "mpld3data-" + obj.props[dataKey];
      var brush = fig.getBrush();

      // Label all data points & find data in each axes
      var dataByAx = [];
      fig.axes.forEach(function(ax){
         var axData = [];
         ax.elements.forEach(function(el){
            if(el.props[dataKey] === obj.props[dataKey]){
               el.group.classed(dataClass, true);
               axData.push(el);
            }
         });
         dataByAx.push(axData);
      });

      // For fast brushing, precompute a list of selection properties
      // properties to apply to the selction.
      var allData = [];
      var dataToBrush = fig.canvas.selectAll("." + dataClass)
                           .each(function(){
                              for(var i=0; i<fig.axes.length; i++){
                                var ax = fig.axes[i];
                                for(var j=0; j<ax.elements.length; j++){
                                  var el = ax.elements[j];
                                  if("group" in el && el.group[0][0] === this){
                                    allData.push({i_ax: i,
                                                  ix: el.props.xindex,
                                                  iy: el.props.yindex});
                                    return;
                                  }
                                }
                              }
                            });
      dataToBrush.data(allData);

      var currentAxes;

      function brushstart(d){
        if(currentAxes != this){
          d3.select(currentAxes).call(brush.clear());
          currentAxes = this;
          brush.x(d.xdom).y(d.ydom);
        }
      }

      function brushmove(d){
        var data = dataByAx[d.axnum];
        if(data.length > 0){
          var ix = data[0].props.xindex;
          var iy = data[0].props.yindex;
          var e = brush.extent();
          if (brush.empty()){
             dataToBrush.selectAll("path").classed("mpld3-hidden", false);
          } else {
             dataToBrush.selectAll("path")
                        .classed("mpld3-hidden",
                            function(p) {
                                return e[0][0] > p[ix] || e[1][0] < p[ix] ||
                                       e[0][1] > p[iy] || e[1][1] < p[iy];
                            });
          }
        } 
      }

      function brushend(d){
         if (brush.empty()){
             dataToBrush.selectAll("path")
                        .classed("mpld3-hidden", false);
         }
      }

      this.enable = function(){
        this.fig.showBrush(this.extentClass);
        brush.on("brushstart", brushstart)
             .on("brush", brushmove)
             .on("brushend", brushend);
        this.enabled = true;
      }

      this.disable = function(){
        this.fig.hideBrush(this.extentClass);
        this.enabled = false;
      }

      this.disable();
    }
    """

    def __init__(self, points):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedbrush",
                      "id": utils.get_id(points, suffix)}


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

plugins.connect(fig, LinkedBrush(points))

mpld3.save_html(fig, 'tmp.html',
                mpld3_url=mpld3.urls.MPLD3_LOCAL,
                d3_url=mpld3.urls.D3_LOCAL)
