import mpld3
import os
import glob
import matplotlib
from . import export

from nose.plugins.skip import SkipTest
matplotlib.use('Agg')

TEST_PLOT_FILES  = os.path.join(mpld3.BASE_PATH, 'mpld3/test_plots/*.py')

TEST_PLOT_SNAPSHOT_DIR = os.path.join(mpld3.BASE_PATH, 'mpld3/test_plots_snapshots/')

def test_snapshots():
    print("Checking test_plots against stored snapshots")
    plot_files = glob.glob(TEST_PLOT_FILES)

    expected_snapshots = {}
    for plot_file in plot_files:
        plot_snapshot = export.snapshot_path(plot_file, TEST_PLOT_SNAPSHOT_DIR) 
        if not os.path.isfile(plot_snapshot):
            continue
        expected_snapshots[plot_snapshot] = plot_file

    got = export.snapshot_mpld3_plots_consecutive(expected_snapshots.values())
    expected = expected_snapshots.keys()
    message_frmt = "Unexpected plot output in d3: {plot_file} {percent}"
    message_frmt_success  = "Plot test passed: {plot_file}"
    for got, expected in zip(got, expected):  
        percent_diff = export.is_images_identical(got, expected, output_bool=False)
        if percent_diff == 0:
            print(message_frmt_success.format(plot_file=expected_snapshots.get(expected)))
        else:
            print(message_frmt.format(plot_file=expected_snapshots.get(expected), percent=percent_diff))
