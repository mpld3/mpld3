"""Test the custom plugin demoed on
http://jakevdp.github.io/blog/2014/01/10/d3-plugins-truly-interactive/
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins, utils
import jinja2
import json


class LinkedView(plugins.PluginBase):
    """A simple plugin showing how multiple axes can be linked"""
    
    JAVASCRIPT = """
    var LinkedViewPlugin = function(fig, prop){
      this.fig = fig;
      this.prop = mpld3.process_props(this, prop, {},
                                      ["idpts", "idline", "data"]);
    }

    LinkedViewPlugin.prototype.draw = function(){
      var pts = mpld3.get_element(this.prop.idpts);
      var line = mpld3.get_element(this.prop.idline);
      var data = this.prop.data;

      function mouseover(d, i){
        line.data = data[i];
        line.elements().transition()
            .attr("d", line.datafunc(line.data))
            .style("stroke", this.style.fill);
      }
      pts.elements().on("mouseover", mouseover);
    };

    mpld3.register_plugin("linkedview", LinkedViewPlugin);
    """

    def __init__(self, points, line, linedata):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedview",
                      "idpts": utils.get_id(points, suffix),
                      "idline": utils.get_id(line),
                      "data": linedata}

def main():
    fig, ax = plt.subplots(2)

    # scatter periods and amplitudes
    np.random.seed(0)
    P = 0.2 + np.random.random(size=20)
    A = np.random.random(size=20)
    x = np.linspace(0, 10, 100)
    data = np.array([[x, Ai * np.sin(x / Pi)]
                     for (Ai, Pi) in zip(A, P)])
    points = ax[1].scatter(P, A, c=P + A,
                           s=200, alpha=0.5)
    ax[1].set_xlabel('Period')
    ax[1].set_ylabel('Amplitude')

    # create the line object
    lines = ax[0].plot(x, 0 * x, '-w', lw=3, alpha=0.5)
    ax[0].set_ylim(-1, 1)

    ax[0].set_title("Hover over points to see lines")

    # transpose line data and add plugin
    linedata = data.transpose(0, 2, 1).tolist()
    plugins.connect(fig, LinkedView(points, lines[0], linedata))

    return fig


if __name__ == '__main__':
    main()
    plt.show()
