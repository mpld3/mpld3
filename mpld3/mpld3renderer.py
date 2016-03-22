"""
mpld3 renderer
==============

This is the renderer class which implements the mplexporter framework for mpld3
"""
__all__ = ["MPLD3Renderer"]

import random
import json
import jinja2
import itertools

import numpy as np

from .mplexporter.utils import color_to_hex
from .mplexporter.exporter import Exporter
from .mplexporter.renderers import Renderer

from .utils import get_id
from .plugins import get_plugins


class MPLD3Renderer(Renderer):
    """Renderer class for mpld3

    This renderer class plugs into the ``mplexporter`` package in order to
    convert matplotlib figures into a JSON-serializable dictionary
    representation which can be read by mpld3.js.
    """
    def __init__(self):
        self.figure_json = None
        self.axes_json = None
        self.finished_figures = []

    @staticmethod
    def datalabel(i):
        return "data{0:02d}".format(i)

    def add_data(self, data, key="data"):
        """Add a dataset to the current figure

        If the dataset matches any already added data, we use that instead.

        Parameters
        ----------
        data : array_like
            a shape [N,2] array of data
        key : string (optional)
            the key to use for the data

        Returns
        -------
        datadict : dictionary
            datadict has the keys "data", "xindex", "yindex", which will
            be passed to the mpld3 JSON object.
        """
        # Check if any column of the data exists elsewhere
        # If so, we'll use that dataset rather than duplicating it.
        data = np.asarray(data)
        if data.ndim != 2 and data.shape[1] != 2:
            raise ValueError("Data is expected to be of size [N, 2]")

        for (i, d) in enumerate(self.datasets):
            if data.shape[0] != d.shape[0]:
                continue

            matches = np.array([np.all(col == d.T, axis=1) for col in data.T])
            if not np.any(matches):
                continue

            # If we get here, we've found a dataset with a matching column
            # we'll update this data with additional columns if necessary
            new_data = list(self.datasets[i].T)
            indices = []
            for j in range(data.shape[1]):
                whr = np.where(matches[j])[0]
                if len(whr):
                    indices.append(whr[0])
                else:
                    # append a new column to the data
                    new_data.append(data[:, j])
                    indices.append(len(new_data) - 1)

            self.datasets[i] = np.asarray(new_data).T
            datalabel = self.datalabel(i + 1)
            xindex, yindex = map(int, indices)
            break
        else:
            # else here can be thought of as "if no break"
            # if we get here, then there were no matching datasets
            self.datasets.append(data)
            datalabel = self.datalabel(len(self.datasets))
            xindex = 0
            yindex = 1

        self.datalabels.append(datalabel)
        return {key: datalabel, "xindex": xindex, "yindex": yindex}

    def open_figure(self, fig, props):
        self.datasets = []
        self.datalabels = []
        self.figure_json = dict(width=props['figwidth'] * props['dpi'],
                                height=props['figheight'] * props['dpi'],
                                axes=[],
                                data={},
                                id=get_id(fig))

    def close_figure(self, fig):
        additional_css = []
        additional_js = []
        for i, dataset in enumerate(self.datasets):
            datalabel = self.datalabel(i + 1)
            self.figure_json['data'][datalabel] = np.asarray(dataset).tolist()
        self.figure_json["plugins"] = []
        for plugin in get_plugins(fig):
            self.figure_json["plugins"].append(plugin.get_dict())
            additional_css.append(plugin.css())
            additional_js.append(plugin.javascript())
        self.finished_figures.append((fig, self.figure_json,
                                      "".join(additional_css),
                                      "".join(additional_js)))

    def open_axes(self, ax, props):
        self.axes_json = dict(bbox=props['bounds'],
                              xlim=props['xlim'],
                              ylim=props['ylim'],
                              xdomain=props['xdomain'],
                              ydomain=props['ydomain'],
                              xscale=props['xscale'],
                              yscale=props['yscale'],
                              axes=props['axes'],
                              axesbg=props['axesbg'],
                              axesbgalpha=props['axesbgalpha'],
                              zoomable=bool(props['dynamic']),
                              id=get_id(ax),
                              lines=[],
                              paths=[],
                              markers=[],
                              texts=[],
                              collections=[],
                              images=[])
        self.figure_json['axes'].append(self.axes_json)

        # Get shared axes info
        xsib = ax.get_shared_x_axes().get_siblings(ax)
        ysib = ax.get_shared_y_axes().get_siblings(ax)
        self.axes_json['sharex'] = [get_id(axi) for axi in xsib
                                    if axi is not ax]
        self.axes_json['sharey'] = [get_id(axi) for axi in ysib
                                    if axi is not ax]

    def close_axes(self, ax):
        self.axes_json = None

    # If draw_line() is not implemented, it will be delegated to draw_path
    # Should we get rid of this? There's not really any advantage here
    def draw_line(self, data, coordinates, style, label, mplobj=None):
        line = self.add_data(data)
        line['coordinates'] = coordinates
        line['id'] = get_id(mplobj)
        for key in ['color', 'linewidth', 'dasharray', 'alpha', 'zorder']:
            line[key] = style[key]
        if 'drawstyle' in style:
            line['drawstyle'] = style['drawstyle']
        
        # Some browsers do not accept dasharray="10,0"
        # This should probably be addressed in mplexporter.
        if line['dasharray'] == "10,0":
            line['dasharray'] = "none"

        self.axes_json['lines'].append(line)

    def draw_path(self, data, coordinates, pathcodes, style,
                  offset=None, offset_coordinates="data", mplobj=None):
        path = self.add_data(data)
        path['coordinates'] = coordinates
        path['pathcodes'] = pathcodes
        path['id'] = get_id(mplobj)
        if offset is not None:
            path['offset'] = list(offset)
            path['offsetcoordinates'] = offset_coordinates

        for key in ['dasharray', 'alpha', 'facecolor',
                    'edgecolor', 'edgewidth', 'zorder']:
            path[key] = style[key]
        
        # Some browsers do not accept dasharray="10,0"
        # This should probably be addressed in mplexporter.
        if path['dasharray'] == "10,0":
            path['dasharray'] = "none"

        self.axes_json['paths'].append(path)

    # If draw_markers is not implemented, it will be delegated to draw_path
    def draw_markers(self, data, coordinates, style, label, mplobj=None):
        markers = self.add_data(data)
        markers["coordinates"] = coordinates
        markers['id'] = get_id(mplobj, 'pts')
        for key in ['facecolor', 'edgecolor', 'edgewidth',
                    'alpha', 'zorder']:
            markers[key] = style[key]
        if style.get('markerpath'):
            vertices, codes = style['markerpath']
            markers['markerpath'] = (vertices.tolist(), codes)
        self.axes_json['markers'].append(markers)

    # If draw_path_collection is not implemented,
    # it will be delegated to draw_path
    def draw_path_collection(self, paths, path_coordinates, path_transforms,
                             offsets, offset_coordinates, offset_order,
                             styles, mplobj=None):
        if len(paths) != 0:
            styles = dict(alphas=[styles['alpha']],
                          edgecolors=[color_to_hex(ec)
                                      for ec in styles['edgecolor']],
                          facecolors=[color_to_hex(fc)
                                      for fc in styles['facecolor']],
                          edgewidths=styles['linewidth'],
                          offsetcoordinates=offset_coordinates,
                          pathcoordinates=path_coordinates,
                          zorder=styles['zorder'])

            pathsdict = self.add_data(offsets, "offsets")
            pathsdict['paths'] = [(v.tolist(), p) for (v, p) in paths]
            pathsdict['pathtransforms'] = [(t[0, :2].tolist()
                                            + t[1, :2].tolist()
                                            + t[2, :2].tolist())
                                           for t in path_transforms]
            pathsdict.update(styles)
            pathsdict['id'] = get_id(mplobj)
            self.axes_json['collections'].append(pathsdict)

    def draw_text(self, text, position, coordinates, style,
                  text_type=None, mplobj=None):
        text = dict(text=text,
                    position=tuple(position),
                    coordinates=coordinates,
                    h_anchor=TEXT_HA_DICT[style['halign']],
                    v_baseline=TEXT_VA_DICT[style['valign']],
                    rotation=-style['rotation'],
                    fontsize=style['fontsize'],
                    color=style['color'],
                    alpha=style['alpha'],
                    zorder=style['zorder'],
                    id=get_id(mplobj))
        self.axes_json['texts'].append(text)

    def draw_image(self, imdata, extent, coordinates, style, mplobj=None):
        image = dict(data=imdata, extent=extent, coordinates=coordinates)
        image.update(style)
        image['id'] = get_id(mplobj)
        self.axes_json['images'].append(image)


TEXT_VA_DICT = {'bottom': 'auto',
                'baseline': 'auto',
                'center': 'central',
                'top': 'hanging'}
TEXT_HA_DICT = {'left': 'start',
                'center': 'middle',
                'right': 'end'}
