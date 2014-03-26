"""
Tools to help with setup.py

Much of this is based on tools in the IPython project:
http://github.com/ipython/ipython
"""

import os
import subprocess
import sys
import shutil


try:
    from setuptools import Command
except:
    from distutils.cmd import Command


SUBMODULES = ['mplexporter']
SUBMODULE_SYNC_PATHS = [('mplexporter/mplexporter', 'mpld3/')]


def is_repo(d):
    """is d a git repo?"""
    return os.path.exists(os.path.join(d, '.git'))


def check_submodule_status(root=None):
    """check submodule status

    Has three return values:

    'missing' - submodules are absent
    'unclean' - submodules have unstaged changes
    'clean' - all submodules are up to date
    """
    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))

    if hasattr(sys, "frozen"):
        # frozen via py2exe or similar, don't bother
        return 'clean'

    if not is_repo(root):
        # not in git, assume clean
        return 'clean'

    for submodule in SUBMODULES:
        if not os.path.exists(submodule):
            return 'missing'

    # Popen can't handle unicode cwd on Windows Python 2
    if sys.platform == 'win32' and sys.version_info[0] < 3 \
       and not isinstance(root, bytes):
        root = root.encode(sys.getfilesystemencoding() or 'ascii')
    # check with git submodule status
    proc = subprocess.Popen('git submodule status',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            cwd=root,
                        )
    status, _ = proc.communicate()
    status = status.decode("ascii", "replace")

    for line in status.splitlines():
        if line.startswith('-'):
            return 'missing'
        elif line.startswith('+'):
            return 'unclean'

    return 'clean'


def update_submodules(repo_dir):
    """update submodules in a repo"""
    subprocess.check_call("git submodule init", cwd=repo_dir, shell=True)
    subprocess.check_call("git submodule update --recursive",
                          cwd=repo_dir, shell=True)


def sync_submodules(repo_dir):
    for source, dest in SUBMODULE_SYNC_PATHS:
        source = os.path.join(repo_dir, source)
        dest = os.path.join(repo_dir, dest)
        print("rsync -r {0} {1}".format(source, dest))
        subprocess.check_call(["rsync", "-r", source, dest])


def require_clean_submodules(repo_dir, argv):
    """Check on git submodules before distutils can do anything

    Since distutils cannot be trusted to update the tree
    after everything has been set in motion,
    this is not a distutils command.
    """
    # Only do this if we are in the git source repository.
    if not is_repo(repo_dir):
        return

    # don't do anything if nothing is actually supposed to happen
    for do_nothing in ('-h', '--help', '--help-commands',
                       'clean', 'submodule', 'buildjs'):
        if do_nothing in argv:
            return

    status = check_submodule_status(repo_dir)

    if status == "missing":
        print("checking out submodules for the first time")
        update_submodules(repo_dir)
    elif status == "unclean":
        print('\n'.join([
            "Cannot build / install mpld3 with unclean submodules",
            "Please update submodules with",
            "    python setup.py submodule",
            "or",
            "    git submodule update",
            "or commit any submodule changes you have made."
        ]))
        sys.exit(1)

    sync_submodules(repo_dir)


class UpdateSubmodules(Command):
    """Update git submodules"""
    description = "Update git submodules"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        failure = False
        try:
            self.spawn('git submodule init'.split())
            self.spawn('git submodule update --recursive'.split())
        except Exception as e:
            failure = e
            print(e)

        if not check_submodule_status() == 'clean':
            print("submodules could not be checked out")
            sys.exit(1)


def _get_js_libs(version, root=None):
    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))
    return [os.path.join(root, "mpld3", "js", lib.format(version))
            for lib in ('mpld3.v{0}.js', 'mpld3.v{0}.min.js')]


def _get_js_sources(root=None, srcdir=None):
    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))

    if srcdir is None:
        srcdir = os.path.join(root, 'src')

    sources = [os.path.join(root, 'package.json')]
    for (directory, subdirs, flist) in os.walk(srcdir):
        sources.extend([os.path.join(directory, f)
                        for f in flist if f.endswith('.js')])
    return sources


def check_js_build_status(root=None, srcdir=None):
    """check status of javascript build

    Has three return values:

    'ok' - JS libraries are built and sources absent or not modified
    'modified' - JS sources present and modified
    'missing' - JS libraries not present and sources not available
    """
    # fix this: can this fail with strange python paths?
    import mpld3
    version = mpld3.__version__

    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))

    if srcdir is None:
        srcdir = os.path.join(root, 'src')

    if hasattr(sys, "frozen"):
        # frozen via py2exe or similar, don't bother
        return 'ok'

    # Check existence of libraries and sources
    if not os.path.exists(srcdir):
        # no javascript sources
        if not all(map(os.path.exists, _get_js_libs(version, root))):
            return 'missing'
        else:
            return 'ok'

    # sources and libs are present: check modification times
    sources = _get_js_sources(root, srcdir)
    libs = _get_js_libs(version, root)

    last_modified_src = max([os.stat(f).st_mtime for f in sources])
    first_modified_lib = min([os.stat(f).st_mtime for f in libs])

    if last_modified_src > first_modified_lib:
        return 'modified'
    else:
        return 'ok'


def build_js_libs(root=None):
    """Build the javascript libraries from sources using smash and uglify.

    This requires npm, and requires that npm install has been run in the
    package directory.
    """
    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(root, 'node_modules', '.bin')):
        raise ValueError("In order to build javascript libraries, you must "
                         "first run `npm install` in the root directory of "
                         "the repository.")

    subprocess.check_call('make javascript', cwd=root, shell=True)


def require_js_libs(repo_dir, argv):
    """Check on javascript libraries before distutils can do anything

    Since distutils cannot be trusted to update the tree
    after everything has been set in motion,
    this is not a distutils command.
    """
    # Only do this if we are in the git source repository.
    if not is_repo(repo_dir):
        return

    # don't do anything if nothing is actually supposed to happen
    for do_nothing in ('-h', '--help', '--help-commands',
                       'clean', 'submodule', 'buildjs'):
        if do_nothing in argv:
            return

    status = check_js_build_status(repo_dir)

    if status == "missing":
        print("Fatal: Javascript libraries and sources are missing")
        sys.exit(1)
    elif status == "modified":
        print("mpld3 javascript sources must be updated before mpld3\n"
              "can be built or installed.  Please run\n"
              "   python setup.py buildjs\n"
              "or\n"
              "   make javascript\n"
              "Note that this requires `npm install` to be run first.")
        sys.exit(1)
    elif not os.path.exists(os.path.join(repo_dir, 'node_modules', '.bin')):
        print("In order to build javascript libraries, you must first run\n"
              "`npm install` in the root directory of the repository.")
        sys.exit(1)


class BuildJavascript(Command):
    """Build the javascript libraries"""
    description = "Build the mpld3 javascript libraries"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        failure = False
        try:
            self.spawn('make javascript'.split())
        except Exception as e:
            failure = e
            print(e)

        if not check_js_build_status() == 'ok':
            print("javascript libraries could not be built")
            sys.exit(1)
