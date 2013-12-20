import os
import glob
from mpld3 import fig_to_d3

import matplotlib
matplotlib.use('Agg') #don't display plots
import pylab as plt

def combine_testplots(wildcard='test_plots/*.py',
                      outfile='test_plots.html',
                      d3_location=None):
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
            fig_html.append(fig_to_d3(fig, d3_location))

    print "writing results to {0}".format(outfile)
    template = '<html>\n{content}\n</html>'
    with open(outfile, 'w') as f:
        f.write('<html>\n\n')
        for fig in fig_html:
            f.write(fig)
        f.write('\n\n</html>')


if __name__ == '__main__':
    import sys
    d3_location = None if len(sys.argv) == 1 else sys.argv[1]
    combine_testplots(wildcard='test_plots/*.py',
                      outfile='test_plots.html',
                      d3_location=d3_location)
