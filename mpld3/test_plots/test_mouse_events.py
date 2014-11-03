"""Plot to test mouse events"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3, mpld3.plugins as plugins


class ClickInfo(plugins.PluginBase):
    """Plugin for getting info on click"""

    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id"];
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        obj.elements().on("click",
                          function(d, i){alert("clicked on points[" + i + "]");});
    }
    """
    def __init__(self, points):
        self.dict_ = {"type": "clickinfo",
                      "id": mpld3.utils.get_id(points)}

def create_plot():
    fig, ax = plt.subplots()
    points = ax.scatter(np.random.rand(50), np.random.rand(50),
                        s=500, alpha=0.3)

    plugins.clear(fig)
    plugins.connect(fig, plugins.Reset(), plugins.Zoom(), ClickInfo(points))
    return fig


def test_mouse_events():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
