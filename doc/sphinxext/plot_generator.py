import sys
import os
import glob
import token
import tokenize
import shutil

import matplotlib
matplotlib.use('Agg')  # don't display plots

import mpld3
from matplotlib import image


class disable_mpld3(object):
    """Context manager to temporarily disable mpld3 show_d3() command"""
    def __enter__(self):
        self.show_d3 = mpld3.show_d3
        mpld3.show_d3 = lambda *args, **kwargs: None
        return self

    def __exit__(self, type, value, traceback):
        mpld3.show_d3 = self.show_d3


RST_TEMPLATE = """
.. _{sphinx_tag}:

{docstring}

.. raw:: html
    {img_html}

**Python source code:** :download:`[download source: {fname}]<{fname}>`

.. literalinclude:: {fname}
    :lines: {end_line}-
"""


INDEX_TEMPLATE = """

.. raw:: html

    <style type="text/css">
    .figure {{
        float: left;
        margin: 10px;
        width: auto;
        height: 200px;
        width: 180px;
    }}

    .figure img {{
        display: inline;
    }}

    .figure .caption {{
        width: 170px;
        text-align: center !important;
    }}
    </style>

.. _{sphinx_tag}:

Example Gallery
===============

{toctree}

{contents}

.. raw:: html

    <div style="clear: both"></div>
"""


def create_thumbnail(infile, thumbfile, scale=0.2,
                     max_width=200, max_height=200,
                     interpolation='bilinear'):
    """
    Create a thumbnail of an image
    """
    basedir, basename = os.path.split(infile)
    baseout, extout = os.path.splitext(thumbfile)

    im = image.imread(infile)
    rows, cols, depth = im.shape

    # this doesn't really matter, it will cancel in the end, but we
    # need it for the mpl API
    dpi = 100

    scale = min(scale, max_height / float(rows))
    scale = min(scale, max_width / float(cols))

    height = float(rows) / dpi * scale
    width = float(cols) / dpi * scale

    extension = extout.lower()

    if extension == '.png':
        from matplotlib.backends.backend_agg \
            import FigureCanvasAgg as FigureCanvas
    elif extension == '.pdf':
        from matplotlib.backends.backend_pdf \
            import FigureCanvasPDF as FigureCanvas
    elif extension == '.svg':
        from matplotlib.backends.backend_svg \
            import FigureCanvasSVG as FigureCanvas
    else:
        raise ValueError("Can only handle extensions 'png', 'svg' or 'pdf'")

    from matplotlib.figure import Figure
    fig = Figure(figsize=(width, height), dpi=dpi)
    canvas = FigureCanvas(fig)

    ax = fig.add_axes([0, 0, 1, 1], aspect='auto',
                      frameon=False, xticks=[], yticks=[])

    basename, ext = os.path.splitext(basename)
    ax.imshow(im, aspect='auto', resample=True,
              interpolation='bilinear')
    fig.savefig(thumbfile, dpi=dpi)
    return fig


def indent(s, N=4):
    """indent a string"""
    return s.replace('\n', '\n' + N * ' ')


class ExampleGenerator(object):
    """Tools for generating an example page from a file"""
    def __init__(self, filename, target_dir):
        self.filename = filename
        self.target_dir = target_dir
        self.extract_docstring()
        self.exec_file()

    @property
    def dirname(self):
        return os.path.split(self.filename)[0]

    @property
    def fname(self):
        return os.path.split(self.filename)[1]

    @property
    def modulename(self):
        return os.path.splitext(self.fname)[0]

    @property
    def pyfilename(self):
        return self.modulename + '.py'

    @property
    def rstfilename(self):
        return self.modulename + ".rst"

    @property
    def htmlfilename(self):
        return self.modulename + '.html'

    @property
    def pngfilename(self):
        return self.modulename + '.png'

    @property
    def sphinxtag(self):
        return self.modulename

    def extract_docstring(self):
        """ Extract a module-level docstring
        """
        lines = open(self.filename).readlines()
        start_row = 0
        if lines[0].startswith('#!'):
            lines.pop(0)
            start_row = 1

        docstring = ''
        first_par = ''
        tokens = tokenize.generate_tokens(lines.__iter__().next)
        for tok_type, tok_content, _, (erow, _), _ in tokens:
            tok_type = token.tok_name[tok_type]
            if tok_type in ('NEWLINE', 'COMMENT', 'NL', 'INDENT', 'DEDENT'):
                continue
            elif tok_type == 'STRING':
                docstring = eval(tok_content)
                # If the docstring is formatted with several paragraphs,
                # extract the first one:
                paragraphs = '\n'.join(line.rstrip()
                                       for line in docstring.split('\n')
                                       ).split('\n\n')
                if len(paragraphs) > 0:
                    first_par = paragraphs[0]
            break

        self.docstring = docstring
        self.short_desc = first_par
        self.end_line = erow + 1 + start_row

    def exec_file(self):
        print("running {0}".format(self.filename))
        with disable_mpld3():
            import matplotlib.pyplot as plt
            plt.close('all')
            my_globals = {'pl': plt,
                          'plt': plt}
            execfile(self.filename, my_globals)

        fig = plt.gcf()
        self.html = mpld3.fig_to_d3(fig)
        thumbfile = os.path.join(self.target_dir,
                                 self.pngfilename)
        fig.savefig(thumbfile)
        create_thumbnail(thumbfile, thumbfile)

    def toctree_entry(self):
        return "   ./%s\n\n" % os.path.splitext(self.htmlfilename)[0]

    def contents_entry(self):
        return (".. figure:: ./{0}\n"
                "    :target: ./{1}\n"
                "    :align: center\n\n"
                "    :ref:`{2}`\n\n".format(self.pngfilename,
                                            self.htmlfilename,
                                            self.sphinxtag))


def main(app):
    target_dir = os.path.join(app.builder.srcdir, 'examples')
    source_dir = os.path.abspath(os.path.join(app.builder.srcdir,
                                              '..', 'examples'))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    toctree = ("\n\n"
               ".. toctree::\n"
               "   :hidden:\n\n")
    contents = "\n\n"

    # Write individual example files
    for filename in glob.glob(os.path.join(source_dir, "*.py")):
        ex = ExampleGenerator(filename, target_dir)
        shutil.copyfile(filename, os.path.join(target_dir, ex.pyfilename))
        output = RST_TEMPLATE.format(sphinx_tag=ex.sphinxtag,
                                     docstring=ex.docstring,
                                     end_line=ex.end_line,
                                     fname=ex.pyfilename,
                                     img_html=indent(ex.html, 4))
        with open(os.path.join(target_dir, ex.rstfilename), 'w') as f:
            f.write(output)

        toctree += ex.toctree_entry()
        contents += ex.contents_entry()

    # write index file
    index_file = os.path.join(target_dir, 'index.rst')
    with open(index_file, 'w') as index:
        index.write(INDEX_TEMPLATE.format(sphinx_tag="example-gallery",
                                          toctree=toctree,
                                          contents=contents))


def setup(app):
    app.connect('builder-inited', main)
