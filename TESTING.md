# Installing snapshot tests

There are a number of tests setup for this codebase. One of them is a tool which compares images of graphs produced by mpld3 against previous versions.

You need to install node and puppeteer.

1. Install Node: https://nodejs.org/en/download/
2. Install puppeteer: 

`npm i`

# Running Tests

To run the tests that confirm plots are as they should be run:

`HIDE_PLOTS=True nosetests mpld3/tests/test_d3_snapshots.py`

# Updating Snapshots 

To update the snapshots:
1) Confirm that the outputs from `visualize_tests.py` are as expected 
2) Then delete the folder `_d3_snapshots` 
3) Run the command:
  `python snapshot.py`

This will create a set of images from the plots in `mpld3/test_plots/` and save those images to `_d3_snapshots/*.jpeg`
4) Cut/paste the files `_d3_snapshots/*.jpeg` to `mpld3/test_plots_snapshots/`
