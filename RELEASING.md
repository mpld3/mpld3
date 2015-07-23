Notes on Releasing mpld3
========================
Cutting a release of mpld3 is a bit more complicated than for a normal package,
because there are both Python and Javascript components, and the versioned
javascript components must be simultaneously synced on the web.

The following is the outline of how to cut a new mpld3 release.
For concreteness, we'll assume we're releasing version 0.3
(change this accordingly)

1. Make sure both the mpld3 repository and the mpld3.github.io repository are up-to-date.

2. Change the release number: in ``mpld3/__about__.py``, change the version to 0.3

3. Remove old javascript sources
   ```
   $ git rm mpld3/js/mpld3.*.js
   ```

3. Make the new javascript sources:
   ```
   $ make javascript
   ```
   Confirm that ``src/version.js`` contains the correct version, and that
   ``mpld3/js/mpld3.v0.3.js`` and ``mpld3/js/mpld3.v0.3.min.js`` exist.

4. Double-check that unit tests pass: run Python tests using
   ```
   $ nosetests mpld3
   ```
   and then run javascript tests using
   ```
   $ make test
   ```

5. Examine visual tests, including checking for interactivity.
   ```
   $ python visualize_tests.py --local
   ```
   click, drag, and hover on every plot to make sure that things work as
   expected. If possible, do this in a few browsers: chrome, firefox, safari...

6. Copy the javascript to the separate website repository
   ```
   $ cp mpld3/js/mpld3.*.js ../mpld3.github.io/
   $ cd ../mpld3.github.io/
   $ git commit -m "update javascript version to 0.3"
   $ git push origin master
   ```

7. Run all the visual tests again, using the built version over http
   (i.e. don't use the ``--local`` flag)
   ```
   $ cd ../mpld3/
   $ python visualize_tests.py
   ```
   This is how most users will be accessing the JS libraries with the new
   release.

8. Once all this works, add all the new files to master:
   ```
   $ git add mpld3/__about__.py src/version.js mpld3/js/*.js
   $ git status
   ```
   Next make sure everything looks OK, and then run the following to commit
   the new version, tag the release, and then push it to master.
   ```
   $ git commit -m "update version to 0.3"
   $ git tag -a v0.3 -m "version 0.3 release"
   $ git push origin master
   $ git push origin v0.3
   ```

9. If all looks good, push the results to PYPI (you'll need to be listed as a
   package maintainer to do this)
   ```
   $ python setup.py sdist upload
   ```

10. Make sure everything works: create a new environment and run the visual
    tests again on the pip-installed version.
    ```
    $ conda create -n mpld3-test numpy=1.8 matplotlib=1.3 jinja2=2.7.2 pandas=0.13.1 nose pip
    $ source activate mpld3-test
    $ pip install mpld3
    ```
    Double-check that the appropriate version of mpld3 is installed.
    Now run
    ```
    $ python visualize_tests.py
    ```
    and make sure everything looks as expected.

11. Update the website documentation:
    ```
    $ cd doc
    $ make clean
    $ make html
    $ cp -r _build/html/* ../../mpld3.github.io/
    $ cd ../../mpld3.github.io/
    $ git add .
    $ git commit -m "Update website for version 0.3"
    $ git push origin master
    ```

11. Now we need to switch the development version.

    - Open ``mpld3/__about__.py`` and change the version to ``0.4.dev1``.
    - Type ``git rm mpld3/js/mpld3.*.js`` to remove old javascript
    - Type ``make javascript`` to make the new javascript
    - examine ``src/version.js`` and ``mpld3/js/`` to make sure the new
      versions are correct
    - commit all to master with message ``"update version to 0.4.dev1"``
    - push changes to master

You're finished!
  

   