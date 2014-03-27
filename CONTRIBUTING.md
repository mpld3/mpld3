# Contributing

The [mpld3](https://github.com/jakevdp/mpld3) project welcomes new contributors. 

## How to Contribute Javascript Code

To contribute javascript you must install [nodejs](http://nodejs.org/) which will include **npm**.

1. Fork your own personal mpld3 repository
2. Within the mpld3 repository, run `npm install` to install the mpld3's javascript dependencies
3. Create a new branch to write your new feature in: `git checkout -b FEATURE-BRANCH`
4. The javascript source files are located in the `src` directory, edit or add source files.  If possible, do not edit `src/mpld3.js`. 
5. Run `make javascript` to build the `mpld3.<version>.js` and `mpld3.<version>.min.js` files located in the `mpld3/js` directory.
6. Run `make test` to verify javascript test in the `test` directory still function properly
7. Run `process_testplots.py` to verify changes do not impact existing plots
8. Commit your changes and make a pull request!
