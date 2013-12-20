"""
Generate Test Plots

This script will go through all the plots in the ``test_plots`` directory, and
save them as D3js to a single HTML file for inspection.
"""
import os
import glob
from mpld3 import fig_to_d3

import matplotlib
matplotlib.use('Agg') #don't display plots
import pylab as plt


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
    fig_html = []
    for filename in glob.glob('test_plots/*.py'):
        dirname, fname = os.path.split(filename)
        modulename = os.path.splitext(fname)[0]
        if dirname not in sys.path:
            sys.path.append(dirname)

        f = __import__(modulename)
        if hasattr(f, 'main'):
            print "running {0}".format(filename)
            fig = f.main()
            fig_html.append(fig_to_d3(fig, d3_url))

    print "writing results to {0}".format(outfile)
    template = '<html>\n{content}\n</html>'
    with open(outfile, 'w') as f:
        f.write('<html>\n\n')
        for fig in fig_html:
            f.write(fig)
        f.write('\n\n</html>')


if __name__ == '__main__':
    import sys
    d3_url = None if len(sys.argv) == 1 else sys.argv[1]
    combine_testplots(wildcard='test_plots/*.py',
                      outfile='test_plots.html',
                      d3_url=d3_url)
