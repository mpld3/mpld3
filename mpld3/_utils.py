"""Utility Routines"""
import warnings
import json

from matplotlib.colors import colorConverter
from matplotlib.path import Path


def color_to_hex(color):
    """Convert rgb tuple to hex color code"""
    rgb = colorConverter.to_rgb(color)
    return '#{0:02X}{1:02X}{2:02X}'.format(*(int(255 * c) for c in rgb))


def many_to_one(input_dict):
    """Convert a many-to-one mapping to a one-to-one mapping"""
    return dict((key, val)
                for keys, val in input_dict.items()
                for key in keys)

LINESTYLES = many_to_one({('solid', '-', (None, None)): "10,0",
                          ('dashed', '--'): "6,6",
                          ('dotted', ':'): "2,2",
                          ('dashdot', '-.'): "4,4,2,4",
                          ('', ' ', 'None', 'none'): "none"})


def get_dasharray(obj, i=None):
    """Get an SVG dash array for the given matplotlib linestyle"""
    if obj.__dict__.get('_dashSeq', None) is not None:
        return ','.join(map(str, obj._dashSeq))
    else:
        ls = obj.get_linestyle()
        if i is not None:
            ls = ls[i]

        dasharray = LINESTYLES.get(ls, None)
        if dasharray is None:
            warnings.warn("dash style '{0}' not understood: "
                          "defaulting to solid.".format(ls))
            dasharray = LINESTYLES['-']
        return dasharray


MARKER_SHAPES = {'o': 'circle',
                 '^': 'triangle-up',
                 'v': 'triangle-down',
                 '+': 'cross',
                 'd': 'diamond',
                 's': 'square'}


def get_d3_shape_for_marker(marker):
    """
    Convert a matplotlib marker ('+','o',...) into a d3 shape name.
    There are fewer to choose from so we're overloading and falling
    back to circle.
    https://github.com/mbostock/d3/wiki/SVG-Shapes#wiki-symbol_type
    """
    if marker in MARKER_SHAPES:
        return MARKER_SHAPES[marker]
    else:
        warnings.warn("""
            Only markers 'o' (circle), '^' (triangle-up),
            'v' (triangle-down), '+' (cross), 'd' (diamond),
            and 's' (square) are currently supported.
            Defaulting to 'circle'.""")
        return 'circle'


PATH_DICT = {Path.LINETO: 'L',
             Path.MOVETO: 'M',
             Path.STOP: 'STOP',
             Path.CURVE3: 'S',
             Path.CURVE4: 'C',
             Path.CLOSEPOLY: 'Z'}


def construct_svg_path(path, transform=None):
    """Construct an SVG path from a (transformed) matplotlib path"""
    if transform is None:
        transform = IdentityTransform()

    steps = []
    for vert, code in path.iter_segments():
        vert = transform.transform(vert.reshape(-1, 2)).ravel()
        step = PATH_DICT[code]
        if step != 'Z':
            step += ' '.join(map(str, vert))
        steps.append(step)

    return ' '.join(steps)


def path_data(path, transform=None):
    if transform is not None:
        path = path.transformed(transform)

    return [(PATH_DICT[path_code], vertices.tolist())
            for vertices, path_code in path.iter_segments()]


class Bunch(dict):
    """Bunch is a simple dictionary wrapper which makes keys into attributes"""
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("No attribute {0}".format(attr))


def collection_data(data, defaults):
    """Prepare collection data.

    data and defaults are dictionaries

    Returns processed data and defaults
    """
    data_out = {}
    defaults_out = dict((key, val) for key, val in defaults.items())

    N = max(len(d) if hasattr(d, '__len__') else 0
            for d in data.values())

    for key, val in data.items():
        defaults_out[key] = defaults.get(key, 'null')
        if val is None:
            if key not in defaults:
                raise ValueError("default needed for {0}".format(key))
            defaults_out[key] = defaults[key]
        elif not hasattr(val, '__len__'):
            defaults_out[key] = val
        elif len(val) == 0:
            if key not in defaults:
                raise ValueError("default needed for {0}".format(key))
            defaults_out[key] = defaults[key]
        elif len(val) == 1:
            defaults_out[key] = val[0]
        elif len(val) == N:
            data_out[key] = val
        else:
            raise ValueError("Length of values for {key} "
                             "does not match".format(key=key))

    data_out = [dict((key, data_out[key][i]) for key in data_out)
                for i in range(N)]
    defaults_out = dict([(key, json.dumps(val))
                         for key, val in defaults_out.items()])

    return data_out, Bunch(defaults_out)
