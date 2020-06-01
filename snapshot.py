import matplotlib
import itertools
import glob
matplotlib.use('Agg')  # don't display plots
import matplotlib.pyplot as plt
import subprocess
import argparse
import json 
import mpld3
from visualize_tests import (
    ExecFile,
    JS_TEMPLATE,
    TEMPLATE,
    MPLD3_TEMPLATE
)
import os
import diffimg

def main():
    description = "Run plots thorugh mpld3 and get their d3 sreenshots"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("files", nargs='*', type=str)
    args = parser.parse_args()

    if len(args.files) == 0:
        input_test_files = ['mpld3/test_plots/*.py', 'examples/*.py']
    else:
        input_test_files = args.files

    if isinstance(input_test_files, str):
        filenames = glob.glob(input_test_files)
    else:
        filenames = itertools.chain(*(glob.glob(w) for w in input_test_files))
    mpld3.tests.export.snapshot_multiple_mpld3_plots(plot_filenames=filenames)

if __name__ == '__main__':
     main()
