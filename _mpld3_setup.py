"""
Tools to help with setup.py

Much of this is based on tools in the IPython project:
http://github.com/ipython/ipython
"""

import os
import subprocess
import sys
import warnings


try:
    from setuptools import Command
except:
    from distutils.cmd import Command


SUBMODULES = ['mplexporter']
SUBMODULE_SYNC_PATHS = [('mplexporter/mplexporter', 'mpld3/')]


def get_version():
    """Get the version info from the mpld3 package without importing it"""
    import ast

    with open(os.path.join("mpld3", "__init__.py"), "r") as init_file:
        module = ast.parse(init_file.read())
    
    version = (ast.literal_eval(node.value) for node in ast.walk(module)
               if isinstance(node, ast.Assign)
               and node.targets[0].id == "__version__")
    try:
        return next(version)
    except StopIteration:
        raise ValueError("version could not be located")


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


BUILD_INFO = """
# Please run 
#   python setup.py buildjs
# or
#   make javascript
# to re-build the javascript libraries.
# This requires npm to be installed: see CONTRIBUTING.md for details.
"""

BUILD_WARNING = """
# It appears that the javascript sources may have been modified.
# If this is the case, then the JS libraries should be rebuilt.
#""" + BUILD_INFO


VERSION_ERROR = """
# JS libraries for version {0} are missing.
#""" + BUILD_INFO


def check_js_build_status(version, root=None, srcdir=None):
    """Check the javascript build status.

    Summary:
    - if we're not in the git repo, or if the source directory doesn't exist,
      then do nothing.
    - if the JS libraries do not exist, return an error with a message about
      building them.
    - if the JS sources have been modified, return a warning with a message
      about how to use them to build the libraries.
    """
    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))

    if srcdir is None:
        srcdir = os.path.join(root, 'src')

    # If we're not in the git repo, then we perform no checks
    if not is_repo(root):
        return

    # If the source directory doesn't exist, then perform no checks
    if not os.path.exists(srcdir):
        return

    # these are the built javascript libraries
    js_libs = [os.path.join(root, "mpld3", "js", lib.format(version))
               for lib in ('mpld3.v{0}.js', 'mpld3.v{0}.min.js')]

    # if the js libraries don't exist, then throw an error
    if not all(os.path.exists(lib) for lib in js_libs):
        raise ValueError(VERSION_ERROR.format(version))

    # these are the javascript sources
    js_sources = [os.path.join(root, 'package.json')]
    for (directory, subdirs, flist) in os.walk(srcdir):
        js_sources.extend([os.path.join(directory, f)
                           for f in flist if f.endswith('.js')])

    # if it looks like the sources have been modified, then warn that
    # they should be rebuilt
    last_modified_src = max([os.stat(f).st_mtime for f in js_sources])
    first_modified_lib = min([os.stat(f).st_mtime for f in js_libs])

    if last_modified_src > first_modified_lib:
        warnings.warn(BUILD_WARNING)


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
