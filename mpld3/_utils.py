"""Utility Routines"""
import warnings

from matplotlib.colors import colorConverter
from matplotlib.path import Path


def get_figtext_coordinates(txt):
    """Get figure coordinates of a text instance"""
    return txt.get_transform().transform(txt.get_position())


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
