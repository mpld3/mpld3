"""
Generate Test Plots

This script will go through all the plots in the ``test_plots`` directory, and
save them as D3js to a single HTML file for inspection.
"""
import os
import glob
import sys
from mpld3 import fig_to_d3

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
                      d3_url=None):
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
    """
    if isinstance(wildcard, basestring):
        filenames = glob.glob(wildcard)
    else:
        filenames = sum([glob.glob(w) for w in wildcard], [])

    fig_html = []
    fig_names = []
    for filename in filenames:
        dirname, fname = os.path.split(filename)
        modulename = os.path.splitext(fname)[0]
        if dirname not in sys.path:
            sys.path.append(dirname)

        f = __import__(modulename)
        if hasattr(f, 'main'):
            print "running {0}".format(filename)
            fig = f.main()
            fig_html.append(fig_to_d3(fig, d3_url))

            fig_png = os.path.splitext(filename)[0] + '.png'
            fig.savefig(fig_png)
            fig_names.append("\n<div class='fig'><img src={0}>"
                             "</div>\n".format(fig_png))

    print "writing results to {0}".format(outfile)
    with open(outfile, 'w') as f:
        f.write(TEMPLATE.format(left_col="".join(fig_html),
                                right_col="".join(fig_names)))


def run_main():
    import argparse
    parser = argparse.ArgumentParser(description=("Run files and convert "
                                                  "output to D3"))
    parser.add_argument("files", nargs='*', type=str)
    parser.add_argument("-d", "--d3-url",
                        help="location of d3 library",
                        type=str, default=None)
    parser.add_argument("-o", "--output",
                        help="output filename",
                        type=str, default='test_plots.html')
    args = parser.parse_args()

    if len(args.files) == 0:
        wildcard = 'test_plots/*.py'
    else:
        wildcard = args.files

    combine_testplots(wildcard=wildcard,
                      outfile=args.output,
                      d3_url=args.d3_url)
    return args.output
    

if __name__ == '__main__':
    import webbrowser

    outfile = run_main()
    
    # Open local file (works on OSX; maybe not on other systems)
    webbrowser.open_new('file://localhost' + os.path.abspath(outfile))
