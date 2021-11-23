import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from _mpld3_setup import (require_clean_submodules, UpdateSubmodules,
                          check_js_build_status, BuildJavascript, get_version)

DESCRIPTION = "D3 Viewer for Matplotlib"
LONG_DESCRIPTION = open('README.md').read()
NAME = "mpld3"
AUTHOR = "Jake VanderPlas"
AUTHOR_EMAIL = "jakevdp@cs.washington.edu"
MAINTAINER = "Jake VanderPlas"
MAINTAINER_EMAIL = "jakevdp@cs.washington.edu"
URL = 'http://mpld3.github.com'
DOWNLOAD_URL = 'http://github.com/jakevdp/mpld3'
LICENSE = 'BSD 3-clause'
VERSION = get_version()

# Make sure submodules are updated and synced
root_dir = os.path.abspath(os.path.dirname(__file__))
require_clean_submodules(root_dir, sys.argv)

# Warn if it looks like JS libs need to be built
if 'buildjs' not in sys.argv:
    check_js_build_status(VERSION, root_dir)


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      cmdclass={'submodule': UpdateSubmodules,
                'buildjs': BuildJavascript},
      packages=['mpld3',
                'mpld3/mplexporter',
                'mpld3/mplexporter/renderers'],
      package_data={'mpld3': ['js/*.js']},
      install_requires=["jinja2", "matplotlib"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'],
      )
