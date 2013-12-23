"""Utility Routines"""
import warnings

from matplotlib.colors import colorConverter


def get_figtext_coordinates(txt):
    """Get figure coordinates of a text instance"""
    return txt.get_transform().transform(txt.get_position())


def color_to_hex(color):
    """Convert rgb tuple to hex color code"""
    rgb = colorConverter.to_rgb(color)
    return '#{:02X}{:02X}{:02X}'.format(*(int(255 * c) for c in rgb))


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


# This is still broken...
#def get_svg_path(path):
#    """Get an SVG patch string from a matplotlib path instance"""
#    path_codes = {path.CLOSEPOLY: 'z',
#                  path.CURVE3: 'C',
#                  path.CURVE4: 'C',
#                  path.LINETO: 'L',
#                  path.MOVETO: 'M',
#                  path.STOP: 'S'}
#
#    return ' '.join(sum([[path_codes[c]] + map(str, d)
#                         for d, c in path.iter_segments()], []))
