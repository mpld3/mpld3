import mpld3
import os
import glob

TEST_PLOT_FILES  = os.path.join(mpld3.BASE_PATH, 'mpld3/test_plots/*.py')

TEST_PLOT_SNAPSHOT_DIR = os.path.join(mpld3.BASE_PATH, 'mpld3/test_plots_snapshots/')

def test_snapshots():
    print("Checking test_plots against stored snapshots")
    plot_files = glob.glob(TEST_PLOT_FILES)

    expected_snapshots = {}
    for plot_file in plot_files:
        plot_snapshot = mpld3.export.snapshot_path(plot_file, TEST_PLOT_SNAPSHOT_DIR) 
        if not os.path.isfile(plot_snapshot):
            continue
        expected_snapshots[plot_snapshot] = plot_file

    got = mpld3.export.snapshot_multiple_mpld3_plots(expected_snapshots.values())
    expected = expected_snapshots.keys()
    message_frmt = "Unexpected plot output in d3: {plot_file}"
    for got, expected in zip(got, expected):  
        message = message_frmt.format(plot_file=expected_snapshots.get(expected))
        assert mpld3.export.is_images_identical(got, expected), message 
