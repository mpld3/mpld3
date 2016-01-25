# Contributing

The [mpld3](https://mpld3.github.io) project welcomes new contributors.
The package contains both JavaScript code and Python code, which require slightly different development setups. Details are described below.

## General guidelines

Code contribution is done via github. You can fork and clone the source from the [mpld3 github page](http://github.com/jakevdp/mpld3).
Whether you are working on the JavaScript side, the Python side, or both, we recommend doing the following (for information about how to use GitHub, please see the [GitHub help page](https://help.github.com/)):

1. Register for a GitHub account.

2. Fork the [main mpld3 repository](http://github.com/jakevdp/mpld3), and clone it to your local machine.

3. Create a new branch in which to write your feature: e.g.

         [~]$ git checkout -b my-feature-name

4. Modify the Python and/or JavaScript code to implement your new feature

5. Add tests and/or examples for your feature if applicable (see instructions below)

6. Run JavaScript and/or Python unit tests and make sure they pass (see instructions below)

7. Push your new branch to your fork on GitHub: e.g.

         [~]$ git push origin my-feature-name

8. Go to http://github.com/yourusername/mpld3 and open a pull request against the main mpld3 repository (if you followed the above steps, you should see a big green "Compare and Pull Request" button on your fork's webpage).

One of the mpld3 maintainers will then respond and (hopefully!) merge your contribution into the repository.


## Building the Python Code
The python code is built in the typical manner: you can instally the package in your standard Python path using

    [~]$ python setup.py install

or to build the package locally run

    [~]$ python setup.py build

### mplexporter submodule
If you are building the package within the git repository, there is an additional step that must be taken.
The mpld3 build depends on the the ``mplexporter`` submodule via the ``git submodule`` tool.
This submodule is in a separate git repository, and must be fetched before the build can take place.
To fetch this dependency, you should run

    [~]$ python setup.py submodule

Once the submodule is fetched, it needs to be synced from its location at ``./mplexporter/mplexporter`` into the mpld3 repository at ``mpld3/mplexporter``: this is done automatically when you run ``python setup.py build`` or ``python setup.py install``.
Because mpld3 is a pure Python package, there are no compiled extensions to build, and it can be built and used locally.


## Building the JavaScript code

The JavaScript portion of mpld3 is built from source using the ``smash`` and ``uglify`` tools that are part of [node.js](http://nodejs.org/).
The benefit of this approach is that the code can be organized, validated, and tested before being automatically formatted and compiled into the final JavaScript library.

Because of this build process, any modification of the JavaScript source requires the installation of [npm](https://www.npmjs.org/).
Once the npm executable is installed on your system, run

    [~]$ npm install

in the main directory to set up the development environment.
This install command will parse the file ``package.json``, and from this information, create a directory ``node_modules`` which contains the tools for building and testing the JavaScript side of mpld3.

Though you may be tempted to modify the JavaScript in ``mpld3/js/`` directly, **this is not a good idea** because these files are overwritten in the build process.
Instead, modify the sources in the ``src/`` directory, and then run

    [~]$ python setup.py buildjs

The built libraries will be saved to ``mpld3/js/mpld3.v($VERSION).js`` and ``mpld3/js/mpld3.v($VERSION).min.js``, where ``($VERSION)`` is replaced by the current version defined in ``mpld3/__about__.py``. The mpld3 Python package will link to the matching mpld3 version.

When contributing a JavaScript patch or enhancement, please include **both the JavaScript sources and the built ``mpld3/js/*.js`` libraries**.
This is important so that users who don't wish to modify the JavaScript can install the package without needing ``npm`` and ``nodejs``.
Additionally, if possible please add JavaScript unit tests of your new functionality to the ``test`` directory (see details below).


## Testing the package
Currently, mpld3 has three different levels of testing, though we hope to streamline this in the future:

- There are automated JavaScript tests using [vows](https://www.npmjs.org/package/vows). These should be run if you modify the JavaScript code.
- There are automated Python tests using [nose](http://nose.readthedocs.org). These should be run if you modify the Python code.
- There are manual plot tests using the ``visualize_tests.py`` script in the repository. These should be run if either the Python or JavaScript code is modified.


### Testing Python with nose

There is a set of non-comprehensive unit tests for the Python code which can be run with the command:

    [~]$ nosetests mpld3

To run these, you will need to install the [nose](http://nose.readthedocs.org) test suite, which can be done by running

    [~]$ pip install nose

These tests are in various directories within the Python source tree, for example ``mpld3/mplexporter/tests/``
In addition to running nosetests, you should check any Python modifications using the ``visualize_tests.py`` script, described below.


### Testing JavaScript with vows
Like the Python nosetests, there is a minimal test suite for the mpld3 JavaScript which is controlled with ``npm`` using the ``vows`` package.
The tests can be executed via

    [~]$ npm test

This requires installation of ``npm``, which is described above.
The tests are located in the ``test`` subdirectory of the main repository.
In addition to running the vows tests, before submitting any JavaScript change, you should examine the output of ``visualize_tests.py``, as described below.


### Comprehensive JS/Python Test: ``visualize_tests.py``
Until we can figure out a way to make the automatic tests with ``nose`` and ``vows`` more comprehensive, it is important to actually examine the interactive output of the mpld3 plot.
In order to facilitate this, there is a script in the main directory, ``visualize_tests.py``, which allows the developer a side-by-side comparison of the matplotlib output and mpld3 output for a range of plot types.
These test plots can be viewed by running

    [~]$ python visualize_tests.py --local

This will generate a file ``test_plots.html`` containing embedded pngs and mpld3 scripts.
If your system allows it, the command will finish by automatically opening this file in a web browser.
It is important to open the JavaScript console (see your browser documentation) and check for errors in the JavaScript execution as you interact with the plots.

Note that the ``--local`` argument in the above command assures that the local copies of the JavaScript libraries are used (i.e. the versions in ``mpld3/js/*.js``).
If you omit this argument, the test plots will be run using the mpld3/d3 library versions available on the web at http://mpld3.github.io.

It is sometimes helpful to specify the javascript paths directly, e.g. if building on remote machine and serving HTML separately:

    [~]python visualize_tests.py --mpld3-url mpld3/js/mpld3.v0.3git.js --d3-url mpld3/js/d3.v3.min.js
    [~]python -m SimpleHTTPServer

