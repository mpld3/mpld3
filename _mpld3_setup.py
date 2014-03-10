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

    if not root:
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
        print "rsync -r {0} {1}".format(source, dest)
        subprocess.check_call(["rsync", "-r", source, dest])


def require_clean_submodules(repo_dir, argv):
    """Check on git submodules before distutils can do anything

    Since distutils cannot be trusted to update the tree
    after everything has been set in motion,
    this is not a distutils command.
    """
    # PACKAGERS: Add a return here to skip checks for git submodules
    
    # don't do anything if nothing is actually supposed to happen
    for do_nothing in ('-h', '--help', '--help-commands',
                       'clean', 'submodule'):
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
    """Update git submodules
    
    IPython's external javascript dependencies live in a separate repo.
    """
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
