# Notes on Releasing mpld3

Cutting a release of mpld3 is a bit more complicated than for a normal package,
because there are both Python and Javascript components, and the versioned
Javascript components must be simultaneously synced on the web.

The following is the outline of how to cut a new mpld3 release. For
concreteness, we'll assume we're releasing version 0.3.0 (change this
accordingly).

It's good to make a new release of the npm package even if you haven't made any
Javascript changes, so that it's clear for users that they're on the latest
version.

## Local testing

Double-check that unit tests pass. Run Python tests using `nose2 mpld3`, and then
run Javascript tests using `make test`.

Examine visual tests, including checking for interactivity.

```
$ python visualize_tests.py --local
```

Click, drag, and hover on every plot to make sure that things work as
expected. If possible, do this in a few browsers: Chrome, Firefox, Safari...

## Changing versions and building

* Change the release number: in `mpld3/__about__.py`, change the version to 0.3.0
* Remove old Javascript sources: `git rm mpld3/js/mpld3.*.js`
* Make the new Javascript sources: `make javascript`
* Confirm that `src/version.js` contains the correct version, and that
`mpld3/js/mpld3.v0.3.0.js` and `mpld3/js/mpld3.v0.3.0.min.js` exist.

Now we need to separately build the JS for use with Browserify.

* Go to `mpld3/js/`
* Change the version in `package.json`. In vim you can just e.g. `:%s/v0.2.9/v0.3.0`
* Remove old `dist/` files with `rm dist/*`
* Run `npm run build`

## Updating the website

Copy the Javascript to the separate website repository:

```
cp mpld3/js/mpld3.*.js ../mpld3.github.io/js
cd ../mpld3.github.io/
git add .
git commit -m "update javascript"
git push
```

Update the website documentation. Make sure mpld3 is installed and that the
packages in doc/requirements.txt are also installed. Additionally, make sure
sphinx, nbformat and nbconvert are installed. So, you may need to do something
like this:

```
pip install -r requirements.txt
pip install -r doc/requirements.txt
pip install .
```

Build the documentation:

```
cd doc
make clean
make html
cp -r _build/html/* ../../mpld3.github.io/
cd ../../mpld3.github.io/
git add .
git commit -m "update website for 0.3.0"
git push
```

## Testing with remote JS

Run all the visual tests again, using the version we uploaded to the website, since this
is how most users will be accessing the JS libraries with the new release. Simply
omit the `--local` flag: `python visualize_tests.py`

## Pushing to master

Once all this works, add all the new files to master:

```
git add .
git commit -m "bump to 0.3.0"
git tag -a v0.3.0 -m "Version 0.3.0"
git push && git push --tags
```

## Publishing to PyPI

Once you've confirmed that everything works, you can upload the package to PyPi.
You'll need to be listed as a package maintainer to do this.

You will need to have the `build` and `twine` packages installed.

```
rm dist/*
python -m build
twine upload dist/*
```

## Publishing to npm

Now you can publish the Javascript for use with browserify to npm.

```
cd mpld3/js
npm publish
```

## Switching to a new development version

You probably want to switch to a development version to avoid confusion:

* Open `mpld3/__about__.py` and change the version to `0.3.1-dev`.
* Type `make javascript` to make the new Javascript

You're finished!
