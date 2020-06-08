"""Plot to test ticklabel plugin"""
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins


class TickFormat(plugins.PluginBase):
    """Tick format plugin."""

    JAVASCRIPT = """
    mpld3.register_plugin("tickformat", TickFormat);
    TickFormat.prototype = Object.create(mpld3.Plugin.prototype);
    TickFormat.prototype.constructor = TickFormat;
    function TickFormat(fig, props) {
        mpld3.Plugin.call(this, fig, props);
        fig.setXTicks(3, function(d) {
            return d3.format('.4f')(d);
        });
        fig.setYTicks(10, function(d) {
            return "it's " + d;
        });
    };
    """

    def __init__(self):
        self.dict_ = {"type": "tickformat"}


def create_plot():
    fig, ax = plt.subplots()
    ax.plot([2000, 2050], [1, 2])
    ax.set_title(
        'Test ticklabel plugin (should be different than image!)',
        size=14
    )
    plugins.connect(fig, TickFormat())
    return fig


if __name__ == "__main__":
    mpld3.show(create_plot())
