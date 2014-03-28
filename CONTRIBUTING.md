# Contributing

The [mpld3](https://mpld3.github.io) project welcomes new contributors.
The package contains both javascript code and Python code, which require slightly different development setups.

## General guidelines

Code contribution is done via github. You can fork and clone the source from the [mpld3 github page](http://github.com/jakevdp/mpld3).
Whether you are working on the Javascript side, the Python side, or both, we recommend doing the following (for information about how to use GitHub, please see the [GitHub help page](https://help.github.com/)):

1. Register for a GitHub account.

2. Fork the [main mpld3 repository](http://github.com/jakevdp/mpld3), and clone it to your local machine.

3. Create a new branch in which to write your feature: e.g.

       [~]$ git checkout -b my-feature-name

4. Modify the Python and/or Javascript code to implement your new feature

5. Add tests and/or examples for your feature if applicable (see instructions below)

6. Run javascript and/or Python unit tests and make sure they pass (see instructions below)

7. Push your new branch to your fork on GitHub: e.g.

       [~]$ git push origin my-feature-name

8. Go to http://github.com/yourusername/mpld3 and open a pull request against the main mpld3 repository (if you followed the above steps, you should see a big green "Compare and Pull Request" button on your fork's webpage).

One of the mpld3 maintainers will then respond and (hopefully!) merge your contribution into the repository.

## Building the Python Code
### mplexporter submodule
The Python code depends on the ``mplexporter`` submodule via the ``git submodule`` tool.
Before building the Python source, you should run

    [~]$ python setup.py submodule

or

    [~]$ git submodule update

to fetch this dependency. The Python package can then be built by running

    [~]$ python setup.py build

An important piece of this build is syncing the ``mplexporter`` submodule from the git location at ``./mplexporter/mplexporter`` into the mpld3 repository at ``mpld3/mplexporter``: this is done automatically when you run ``python setup.py build`` or ``python setup.py install``.
Because mpld3 is a pure Python package, there are no compiled extensions to build, and it can be imported and used locally.

### Testing the Python code
There are some non-comprehensive unit tests which can be run with the command

    [~]$ nosetests mpld3

To run these, you will need to install the ``nose`` test suite, which can be done by running

    [~]$ pip install nose

Until we can figure out a way to automate html/javascript tests, a more important check is to run the test plots, which allow the developer a side-by-side comparison of the matplotlib output and mpld3 output for a range of plot types.
These test plots can be viewed by running

    [~]$ python process_testplots.py --local

This will generate a file ``test_plots.html`` containing embedded pngs and mpld3 scripts.
If your system allows it, the command will automatically open this file in a web browser.
It is important to open the javascript console (see your browser documentation) and check for errors in the javascript execution as you interact with the plots.

Note that the ``--local`` argument in the above command assures that the local copies of the javascript libraries are used (i.e. the versions in ``mpld3/js/*.js``).
If you omit this argument, the test plots will be run using the mpld3/d3 library versions available on the web at http://mpld3.github.io.


## Building the Javascript code

The javascript code is built from source using the ``smash`` and ``uglify`` tools that are part of [node.js](http://nodejs.org/).
The benefit of this is that the code can be organized, validated, and tested before being automatically formatted and compiled into the final javascript library.

Because of this, modification of the javascript source requires the installation of [npm](https://www.npmjs.org/).
Once the npm executable is installed on your system, run ``npm install`` in the main directory to set up the development environment.
This will read the file ``package.json``, and from this information, create a directory ``node_modules`` which contains the tools for building and testing the javascript side of mpld3.

Though you may be tempted to modify the javascript in ``mpld3/js/`` directly, **this is not a good idea** because these files are overwritten in the build process.
Instead, modify the sources in the ``src/`` directory, and then run

    [~]$ make javascript

or

    [~]$ python setup.py buildjs

The built libraries will be saved to ``mpld3/js/mpld3.v($VERSION).js`` and ``mpld3/js/mpld3.v($VERSION).min.js``, where ``($VERSION)`` is replaced by the current version defined in ``mpld3/__about__.py``. The mpld3 Python package will link to the matching mpld3 version.

When contributing a javascript change, please include **both the javascript sources and the built ``mpld3/js/*.js`` libraries**.
This is important so that users who don't wish to modify the javascript can install the package without needing ``npm`` and ``nodejs``.

### Testing javascript
Like the Python nosetests, there is a minimal test suite for the mpld3 javascript which is controlled with ``npm`` using the ``vows`` package.
The tests can be executed via

    [~]$ npm test

or
    
    [~]$ make test

Additionally, before submitting any javascript change, you should examine the output of ``process_testplots.py``, as described above.
