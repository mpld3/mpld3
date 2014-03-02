from ..exporter import Exporter
from ..renderers import PlotlyRenderer

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numbers


def test_simple_line():
    fig, ax = plt.subplots()
    ax.plot(range(10), '-k')
    ax.plot(range(5), '.k')

    renderer = PlotlyRenderer()
    exporter = Exporter(renderer)
    exporter.run(fig)
    for data_no, data_dict in enumerate(renderer.data):
        equivalent, msg = compare_dict(data_dict, SIMPLE_LINE['data'][data_no])
        assert equivalent, msg
    equivalent, msg = compare_dict(renderer.layout, SIMPLE_LINE['layout'])
    assert equivalent, msg


def test_subplots():
    fig = plt.figure() # matplotlib.figure.Figure obj
    gs = gridspec.GridSpec(3, 3)
    ax1 = fig.add_subplot(gs[0,:])
    ax1.plot([1,2,3,4,5], [10,5,10,5,10], 'r-')
    ax2 = fig.add_subplot(gs[1,:-1])
    ax2.plot([1,2,3,4], [1,4,9,16], 'k-')
    ax3 = fig.add_subplot(gs[1:, 2])
    ax3.plot([1,2,3,4], [1,10,100,1000], 'b-')
    ax4 = fig.add_subplot(gs[2,0])
    ax4.plot([1,2,3,4], [0,0,1,1], 'g-')
    ax5 = fig.add_subplot(gs[2,1])
    ax5.plot([1,2,3,4], [1,0,0,1], 'c-')

    renderer = PlotlyRenderer()
    exporter = Exporter(renderer)
    exporter.run(fig)
    for data_no, data_dict in enumerate(renderer.data):
        equivalent, msg = compare_dict(data_dict, SUBPLOTS['data'][data_no])
        assert equivalent, msg
    equivalent, msg = compare_dict(renderer.layout, SUBPLOTS['layout'])
    assert equivalent, msg


def compare_dict(dict1, dict2, equivalent=True, msg='', tol_digits=10):
    for key in dict1:
        if key not in dict2:
            return False, "{} not {}".format(dict1.keys(), dict2.keys())
    for key in dict1:
        if isinstance(dict1[key], dict):
            equivalent, msg = compare_dict(dict1[key], dict2[key], tol_digits=tol_digits)
        else:
            if not (dict1[key] == dict2[key]):
                return False, "['{}'] = {} not {}".format(key, dict1[key], dict2[key])
        if not equivalent:
            return False, "['{}']".format(key) + msg
    return equivalent, msg


## dictionaries for tests

SIMPLE_LINE = {
    'data': [{'line': {'color': '#000000', 'dash': 'solid', 'opacity': 1, 'width': 1.0},
              'mode': 'lines',
              'x': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
              'xaxis': 'x',
              'y': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
              'yaxis': 'y'},
             {'marker': {'color': '#000000', 'line': {'color': '#000000', 'width': 0.5},
                         'opacity': 1,
                         'symbol': 'dot'},
              'mode': 'markers',
              'x': [0.0, 1.0, 2.0, 3.0, 4.0],
              'xaxis': 'x',
              'y': [0.0, 1.0, 2.0, 3.0, 4.0],
              'yaxis': 'y'}],
    'layout': {'height': 480,
               'showlegend': False,
               'title': '',
               'width': 640,
               'xaxis': {'domain': [0.125, 0.90000000000000002],
                         'range': (0.0, 9.0),
                         'showgrid': False,
                         'title': '',
                         'anchor': 'y'},
               'yaxis': {'domain': [0.099999999999999978, 0.90000000000000002],
                         'range': (0.0, 9.0),
                         'showgrid': False,
                         'title': '',
                         'anchor': 'x'}}
}

SUBPLOTS = {'data': [{'line': {'color': '#FF0000', 'dash': 'solid', 'opacity': 1, 'width': 1.0},
                      'mode': 'lines',
                      'x': [1.0, 2.0, 3.0, 4.0, 5.0],
                      'y': [10.0, 5.0, 10.0, 5.0, 10.0]},
                     {'line': {'color': '#000000', 'dash': 'solid', 'opacity': 1, 'width': 1.0},
                      'mode': 'lines',
                      'x': [1.0, 2.0, 3.0, 4.0],
                      'xaxis': 'x2',
                      'y': [1.0, 4.0, 9.0, 16.0],
                      'yaxis': 'y2'},
                     {'line': {'color': '#0000FF', 'dash': 'solid', 'opacity': 1, 'width': 1.0},
                      'mode': 'lines',
                      'x': [1.0, 2.0, 3.0, 4.0],
                      'xaxis': 'x3',
                      'y': [1.0, 10.0, 100.0, 1000.0],
                      'yaxis': 'y3'},
                     {'line': {'color': '#007F00', 'dash': 'solid', 'opacity': 1, 'width': 1.0},
                      'mode': 'lines',
                      'x': [1.0, 2.0, 3.0, 4.0],
                      'xaxis': 'x4',
                      'y': [0.0, 0.0, 1.0, 1.0],
                      'yaxis': 'y4'},
                     {'line': {'color': '#00BFBF', 'dash': 'solid', 'opacity': 1, 'width': 1.0},
                      'mode': 'lines',
                      'x': [1.0, 2.0, 3.0, 4.0],
                      'xaxis': 'x5',
                      'y': [1.0, 0.0, 0.0, 1.0],
                      'yaxis': 'y5'}],
            'layout': {'height': 480,
                     'showlegend': False,
                     'title': '',
                     'width': 640,
                     'xaxis': {'anchor': 'y',
                      'domain': [0.125, 0.90000000000000013],
                      'range': (1.0, 5.0),
                      'showgrid': False,
                      'title': ''},
                     'xaxis2': {'anchor': 'y2',
                      'domain': [0.125, 0.62647058823529411],
                      'range': (1.0, 4.0),
                      'showgrid': False,
                      'title': ''},
                     'xaxis3': {'anchor': 'y3',
                      'domain': [0.67205882352941182, 0.90000000000000013],
                      'range': (1.0, 4.0),
                      'showgrid': False,
                      'title': ''},
                     'xaxis4': {'anchor': 'y4',
                      'domain': [0.125, 0.35294117647058826],
                      'range': (1.0, 4.0),
                      'showgrid': False,
                      'title': ''},
                     'xaxis5': {'anchor': 'y5',
                      'domain': [0.39852941176470591, 0.62647058823529411],
                      'range': (1.0, 4.0),
                      'showgrid': False,
                      'title': ''},
                     'yaxis': {'anchor': 'x',
                      'domain': [0.66470588235294115, 0.90000000000000002],
                      'range': (5.0, 10.0),
                      'showgrid': False,
                      'title': ''},
                     'yaxis2': {'anchor': 'x2',
                      'domain': [0.38235294117647056, 0.61764705882352944],
                      'range': (0.0, 16.0),
                      'showgrid': False,
                      'title': ''},
                     'yaxis3': {'anchor': 'x3',
                      'domain': [0.099999999999999867, 0.61764705882352944],
                      'range': (0.0, 1000.0),
                      'showgrid': False,
                      'title': ''},
                     'yaxis4': {'anchor': 'x4',
                      'domain': [0.099999999999999867, 0.33529411764705874],
                      'range': (0.0, 1.0),
                      'showgrid': False,
                      'title': ''},
                     'yaxis5': {'anchor': 'x5',
                      'domain': [0.099999999999999867, 0.33529411764705874],
                      'range': (0.0, 1.0),
                      'showgrid': False,
                      'title': ''}}}