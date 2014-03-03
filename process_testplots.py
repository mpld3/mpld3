"""
Generate Test Plots

This script will go through all the plots in the ``test_plots`` directory, and
save them as D3js to a single HTML file for inspection.
"""
import os
import glob
import sys

from mpld3 import urls, fig_to_html

import matplotlib
matplotlib.use('Agg') #don't display plots
import pylab as plt
plt.rcParams['figure.figsize'] = (6, 4.5)
plt.rcParams['savefig.dpi'] = 80

TEMPLATE = """
<html>
<head>
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
  height: 400px;
}}
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
</body>
</html>
"""


def combine_testplots(wildcard='test_plots/*.py',
                      outfile='test_plots.html',
                      d3_url=None, mpld3_url=None):
    """Generate figures from the plots and save to an HTML file

    Parameters
    ----------
    wildcard : string
        a regex matching files
    outfile : string
        the output HTML file for saving the results
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
        filenames = sum([glob.glob(w) for w in wildcard], [])

    fig_html = []
    fig_png = []
    for filename in filenames:
        dirname, fname = os.path.split(filename)
        modulename = os.path.splitext(fname)[0]
        if dirname not in sys.path:
            sys.path.append(dirname)

        try:
            f = __import__(modulename)
        except Exception as e:
            print("!!!  Exception raised in {0}".format(filename))
            print("!!!   {0}: {1}".format(e.__class__.__name__,
                                          e.message))
            continue

        if hasattr(f, 'main'):
            print("running {0}".format(filename))

            try:
                fig = f.main()
            except Exception as e:
                print("Exception raised in {0}".format(filename))
                print(" {0}: {1}".format(e.__class__.__name__,
                                         e.message))
                fig = None

            if fig is not None:
                fig_html.append("\n<div class='fig'>\n{0}\n</div>"
                                "\n".format(fig_to_html(fig, d3_url=d3_url,
                                                        mpld3_url=mpld3_url)))

                figfile = os.path.splitext(filename)[0] + '.png'
                fig.savefig(figfile)
                fig_png.append("\n<div class='fig'><img src={0}>"
                                 "</div>\n".format(figfile))
                plt.close(fig)

    print("writing results to {0}".format(outfile))
    with open(outfile, 'w') as f:
        f.write(TEMPLATE.format(left_col="".join(fig_html),
                                right_col="".join(fig_png)))


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
                        type=str, default='test_plots.html')
    parser.add_argument("-l", "--local", action="store_true")
    args = parser.parse_args()

    if len(args.files) == 0:
        wildcard = 'test_plots/*.py'
    else:
        wildcard = args.files

    if args.local:
        args.d3_url = urls.D3_LOCAL
        args.mpld3_url = urls.MPLD3_LOCAL

    combine_testplots(wildcard=wildcard,
                      outfile=args.output,
                      d3_url=args.d3_url,
                      mpld3_url=args.mpld3_url)
    return args.output
    

if __name__ == '__main__':
    import webbrowser

    outfile = run_main()
    
    # Open local file (works on OSX; maybe not on other systems)
    webbrowser.open_new('file://localhost' + os.path.abspath(outfile))
