"""
Plotly Renderer
================
This is a renderer class to be used with an exporter for rendering plots in Plotly!
"""
from . import plotly_utils
from .. base import Renderer
from ... exporter import Exporter


class PlotlyRenderer(Renderer):
    def __init__(self, username=None, api_key=None):
        self.output = ""
        self.username = username
        self.api_key = api_key
        self.data = []
        self.layout = {}
        self.axis_ct = 0

    def open_figure(self, fig, props):
        self.output += "opening figure\n"
        self.layout['width'] = int(props['figwidth']*props['dpi'])
        self.layout['height'] = int(props['figheight']*props['dpi'])

    def close_figure(self, fig):
        self.output += "closing figure\n"
        self.configure_primary_axes()  # changes 'y1', 'xaxis1', etc. to 'y', 'xaxis', etc.
        self.layout['showlegend'] = False

    def open_axes(self, ax, props):
        self.axis_ct += 1
        self.output += "  opening axis {}\n".format(self.axis_ct)
        layout = {
            'title': props['title'],
            'xaxis{}'.format(self.axis_ct): {
                'range': props['xlim'],
                'title': props['xlabel'],
                'showgrid': props['xgrid'],
                'domain': plotly_utils.get_x_domain(props['bounds']),
                'anchor': 'y{}'.format(self.axis_ct)
            },
            'yaxis{}'.format(self.axis_ct): {
                'range': props['ylim'],
                'title': props['ylabel'],
                'showgrid': props['ygrid'],
                'domain': plotly_utils.get_y_domain(props['bounds']),
                'anchor': 'x{}'.format(self.axis_ct)
            }
        }
        for key, value in layout.items():
            self.layout[key] = value

    def close_axes(self, ax):
        self.output += "  closing axis {}\n".format(self.axis_ct)

    def draw_line(self, data, coordinates, style, mplobj=None):
        if coordinates == 'data':
            self.output += "    draw line with {0} points\n".format(data.shape[0])
            trace = {
                'mode': 'lines',
                'x': [xy_pair[0] for xy_pair in data],
                'y': [xy_pair[1] for xy_pair in data],
                'xaxis': 'x{}'.format(self.axis_ct),
                'yaxis': 'y{}'.format(self.axis_ct),
                'line': {
                    'opacity': style['alpha'],
                    'color': style['color'],
                    'width': style['linewidth'],
                    'dash': plotly_utils.convert_dash(style['dasharray'])
                }
            }
            self.data += trace,
        else:
            self.output += "    received {}-point line with 'figure' coordinates, skipping!".format(data.shape[0])

    def draw_markers(self, data, coordinates, style, mplobj=None):
        if coordinates == 'data':
            self.output += "    draw {0} markers\n".format(data.shape[0])
            trace = {
                'mode': 'markers',
                'x': [xy_pair[0] for xy_pair in data],
                'y': [xy_pair[1] for xy_pair in data],
                'xaxis': 'x{}'.format(self.axis_ct),
                'yaxis': 'y{}'.format(self.axis_ct),
                'marker': {
                    'opacity': style['alpha'],
                    'color': style['facecolor'],
                    'symbol': plotly_utils.convert_symbol(style['marker']),
                    'line': {
                        'color': style['edgecolor'],
                        'width': style['edgewidth']
                    }
                }
            }
            # not sure whether we need to incorporate style['markerpath']
            self.data += trace,
        else:
            self.output += "    received {} markers with 'figure' coordinates, skipping!".format(data.shape[0])

    def configure_primary_axes(self):
        try:
            for axis_no in range(0, len(self.data)):
                if self.data[axis_no]['xaxis'] == 'x1':
                    del self.data[axis_no]['xaxis']
                if self.data[axis_no]['yaxis'] == 'y1':
                    del self.data[axis_no]['yaxis']
        except KeyError:
            pass
        except IndexError:
            pass
        if 'xaxis1' in self.layout:
            self.layout['xaxis'] = self.layout.pop('xaxis1')
        if 'yaxis1' in self.layout:
            self.layout['yaxis'] = self.layout.pop('yaxis1')
        try:
            if 'y1' in self.layout['xaxis']['anchor']:
                self.layout['xaxis']['anchor'] = 'y'
        except KeyError:
            pass
        try:
            if 'x1' in self.layout['yaxis']['anchor']:
                self.layout['yaxis']['anchor'] = 'x'
        except KeyError:
            pass


def fig_to_plotly(fig, username=None, api_key=None, notebook=False):
    """Convert a matplotlib figure to plotly dictionary

    """
    import plotly
    renderer = PlotlyRenderer(username=username, api_key=api_key)
    Exporter(renderer).run(fig)
    py = plotly.plotly(renderer.username, renderer.api_key)
    if notebook:
        return py.iplot(renderer.data, layout=renderer.layout)
    else:
        py.plot(renderer.data, layout=renderer.layout)
