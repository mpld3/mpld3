"""Test the custom plugin demoed on
http://jakevdp.github.io/blog/2014/01/10/d3-plugins-truly-interactive/
"""
import matplotlib.pyplot as plt
import numpy as np
from mpld3 import plugins
import jinja2
import json


class LinkedView(plugins.PluginBase):
    """A simple plugin showing how multiple axes can be linked"""
    
    FIG_JS = jinja2.Template("""
    var linedata{{ id }} = {{ linedata }};

    ax{{ axid }}.axes.selectAll(".paths{{ collid }}")
	    .on("mouseover", function(d, i){
             line{{ elid }}.data = linedata{{ id }}[i];
             line{{ elid }}.lineobj.transition()
                .attr("d", line{{ elid }}.line(line{{ elid }}.data))
                .style("stroke", this.style.fill);})
    """)

    def __init__(self, points, line, linedata):
        self.points = points
        self.line = line
        self.linedata = linedata
        self.id = self.generate_unique_id()

    def _fig_js_args(self):
        points = self._get_d3obj(self.points)
        line = self._get_d3obj(self.line)
        return dict(id=self.id,
                    axid=points.axid,
                    collid=points.collid,
                    elid=line.elid,
                    lineaxid=line.axid,
                    lineid=line.lineid,
                    linedata=json.dumps(self.linedata))

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
