"""
Visualize Test Plots

This script will go through all the plots in the ``mpld3/test_plots``
directory, and save them as D3js to a single HTML file for inspection.
"""
import os
import glob
import sys
import gc
import traceback
import itertools
import json
import contextlib

import matplotlib

MPLBE = os.environ.get('MPLBE', False)
if MPLBE:
    import matplotlib
    matplotlib.use(MPLBE)

import matplotlib.pyplot as plt

import mpld3
from mpld3 import urls
from mpld3._display import NumpyEncoder
from mpld3.mpld3renderer import MPLD3Renderer
from mpld3.mplexporter import Exporter

plt.rcParams['figure.figsize'] = (6, 4.5)
plt.rcParams['savefig.dpi'] = 80

TEMPLATE = """
<html>
<head>
<script type="text/javascript" src={d3_url}></script>
<script type="text/javascript" src={mpld3_url}></script>
<style type="text/css">
.left_col {{
    float: left;
    width: 50%;
}}

.right_col {{
    margin-left: 50%;
    width: 50%;
}}

.fig {{
  height: 850px;
}}


{extra_css}

</style>
</head>

<body>
<div id="wrap">
    <div class="left_col">
        {left_col}
    </div>
    <div class="right_col">
        {right_col}
    </div>
</div>
<script>
    {js_commands}
</script>
</body>
</html>
"""

MPLD3_TEMPLATE = """
<div>{fname}</div><div class="fig" id="fig{figid:03d}"></div>
"""

JS_TEMPLATE = """
!function(mpld3){{
  {extra_js}
  mpld3.draw_figure("fig{figid:03d}", {figure_json});
}}(mpld3);
"""


@contextlib.contextmanager
def mpld3_noshow():
    """context manager to use mpld3 with show() disabled"""
    import mpld3
    _show = mpld3.show
    mpld3.show = lambda *args, **kwargs: None
    yield mpld3
    mpld3.show = _show


@contextlib.contextmanager
def use_dir(dirname=None):
    """context manager to temporarily change the working directory"""
    cwd = os.getcwd()
    if dirname is None:
        dirname = cwd
    os.chdir(dirname)
    yield
    os.chdir(cwd)


class ExecFile(object):
    """
    Class to execute plotting files, and extract the mpl and mpld3 figures.
    """
    def __init__(self, filename, execute=True, pngdir='_pngs'):
        self.filename = filename
        if execute:
            self.execute_file()
        if not os.path.exists(pngdir):
            os.makedirs(pngdir)
        basename = os.path.splitext(os.path.basename(filename))[0]
        self.pngfmt = os.path.join(pngdir, basename + "_{0:2d}.png")

    def execute_file(self):
        """
        Execute the file, catching matplotlib figures
        """
        dirname, fname = os.path.split(self.filename)
        print('plotting {0}'.format(fname))

        # close any currently open figures
        plt.close('all')

        # close any currently open figures
        plt.close('all')

        with mpld3_noshow() as mpld3:
            with use_dir(dirname):
                try:
                    # execute file, forcing __name__ == '__main__'
                    exec(open(os.path.basename(self.filename)).read(),
                         {'plt': plt, 'mpld3': mpld3, '__name__': '__main__'})
                    gcf = matplotlib._pylab_helpers.Gcf
                    fig_mgr_list = gcf.get_all_fig_managers()
                    self.figlist = sorted([manager.canvas.figure
                                           for manager in fig_mgr_list],
                                          key=lambda fig: fig.number)
                except:
                    print(80 * '_')
                    print('{0} is not compiling:'.format(fname))
                    traceback.print_exc()
                    print(80 * '_')
                finally:
                    ncol = gc.collect()

    def iter_png(self):
        for fig in self.figlist:
            fig_png = self.pngfmt.format(fig.number)
            fig.savefig(fig_png)
            yield fig_png

    def iter_json(self):
        for fig in self.figlist:
            renderer = MPLD3Renderer()
            Exporter(renderer, close_mpl=False).run(fig)
            fig, fig_json, extra_css, extra_js = renderer.finished_figures[0]
            yield (json.dumps(fig_json, cls=NumpyEncoder), extra_js, extra_css)


def combine_testplots(wildcard='mpld3/test_plots/*.py',
                      outfile='_test_plots.html',
                      pngdir='_pngs',
                      d3_url=None, mpld3_url=None):
    """Generate figures from the plots and save to an HTML file

    Parameters
    ----------
    wildcard : string or list
        a regexp or list of regexps matching files to test
    outfile : string
        the path at which the output HTML will be saved
    d3_url : string
        the URL of the d3 library to use.  If not specified, a standard web
        address will be used.
    mpld3_url : string
        the URL of the mpld3 library to use.  If not specified, a standard web
        address will be used.
    """
    if isinstance(wildcard, str):
        filenames = glob.glob(wildcard)
    else:
        filenames = itertools.chain(*(glob.glob(w) for w in wildcard))

    fig_png = []
    fig_json = []
    fig_name = []
    for filename in filenames:
        result = ExecFile(filename, pngdir=pngdir)
        fig_png.extend(result.iter_png())
        for r in result.iter_json():
            fig_json.append(r)
            fig_name.append(filename)

    left_col = [MPLD3_TEMPLATE.format(figid=i, fname=fig_name[i])
                for i in range(len(fig_json))]
    js_commands = [JS_TEMPLATE.format(figid=figid,
                                      figure_json=figjson,
                                      extra_js=figjs)
                   for figid, (figjson, figjs, _) in enumerate(fig_json)]
    right_col = ['<div>png version</div><div class="fig"><img src="{0}"></div>\n'.format(fig)
                 for fig in fig_png]
    extra_css = [tup[2] for tup in fig_json]

    print("writing results to {0}".format(outfile))
    with open(outfile, 'w') as f:
        f.write(TEMPLATE.format(left_col="".join(left_col),
                                right_col="".join(right_col),
                                d3_url=json.dumps(d3_url),
                                mpld3_url=json.dumps(mpld3_url),
                                js_commands="".join(js_commands),
                                extra_css="".join(extra_css)))


def run_main():
    import argparse
    parser = argparse.ArgumentParser(description=("Run files and convert "
                                                  "output to D3"))
    parser.add_argument("files", nargs='*', type=str)
    parser.add_argument("-d", "--d3-url",
                        help="location of d3 library",
                        type=str, default=None)
    parser.add_argument("-m", "--mpld3-url",
                        help="location of the mpld3 library",
                        type=str, default=None)
    parser.add_argument("-o", "--output",
                        help="output filename",
                        type=str, default='_test_plots.html')
    parser.add_argument("-j", "--minjs", action="store_true")
    parser.add_argument("-l", "--local", action="store_true")
    parser.add_argument("-n", "--nolaunch", action="store_true")
    args = parser.parse_args()

    if len(args.files) == 0:
        wildcard = ['mpld3/test_plots/*.py', 'examples/*.py']
    else:
        wildcard = args.files

    if args.d3_url is None:
        args.d3_url = urls.D3_URL
    if args.mpld3_url is None:
        args.mpld3_url = urls.MPLD3_URL

    if args.local:
        args.d3_url = urls.D3_LOCAL
        if args.minjs:
            args.mpld3_url = urls.MPLD3MIN_LOCAL
        else:
            args.mpld3_url = urls.MPLD3_LOCAL
    else:
        if args.minjs:
            args.mpld3_url = urls.MPLD3MIN_URL

    print("d3 url: {0}".format(args.d3_url))
    print("mpld3 url: {0}".format(args.mpld3_url))

    combine_testplots(wildcard=wildcard,
                      outfile=args.output,
                      d3_url=args.d3_url,
                      mpld3_url=args.mpld3_url)
    return args.output, args.nolaunch


if __name__ == '__main__':
    outfile, nolaunch = run_main()

    if not nolaunch:
        # Open local file (works on OSX; maybe not on other systems)
        import webbrowser
        webbrowser.open_new('file://localhost' + os.path.abspath(outfile))
