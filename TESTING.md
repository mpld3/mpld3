# Installing tests

You need to install node and puppeteer.

1. Install Node: https://nodejs.org/en/download/
2. Install puppeteer: 

`npm i`

# Running Tests

To run the tests that confirm plots are as they should be run:

`HIDE_PLOTS=True nosetests mpld3/tests/test_d3_snapshots.py --nocapture`
