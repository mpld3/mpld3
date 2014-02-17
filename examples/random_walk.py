"""
Visualizing Random Walks
========================
This shows the use of transparent lines to visualize random walk data.
Thre is also a custom plugin defined which causes lines to be highlighted
when the mouse hovers over them.
"""
import numpy as np
import matplotlib.pyplot as plt

from mpld3 import plugins, show_d3
import jinja2

class HighlightLines(plugins.PluginBase):
    """A plugin to highlight lines on hover"""

    FIG_JS = jinja2.Template("""
    {% for line in lines %}
      ax{{ line.axid }}.axes.selectAll('.line{{ line.lineid }}')
         .on("mouseover", function(d, i){
                            console.log(d3.select(this));
                            d3.select(this).transition().duration(50)
                                .style("stroke-opacity", 1.0)
                          })
         .on("mouseout", function(d, i){
                            console.log(d3.select(this));
                            d3.select(this).transition().duration(200)
                                .style("stroke-opacity",
                                       {{ line.line.get_alpha() }})
                          });
    {% endfor %}
    """)

    def __init__(self, lines):
        self.lines = lines

    def _fig_js_args(self):
        lines = [self._get_d3obj(line) for line in self.lines]
        return dict(lines=lines)


N_paths = 50
N_steps = 100

x = np.linspace(0, 10, 100)
y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
y = y.cumsum(1)

fig, ax = plt.subplots(subplot_kw={'xticks': [], 'yticks': []})
lines = ax.plot(x, y.T, color='blue', lw=4, alpha=0.1)
plugins.connect(fig, HighlightLines(lines))

show_d3()
