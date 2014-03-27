import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from _mpld3_setup import (require_clean_submodules, UpdateSubmodules,
                          require_js_libs, BuildJavascript)

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

# import mpld3 for version
import mpld3
VERSION = mpld3.__version__

# Make sure submodules are updated and synced
root_dir = os.path.abspath(os.path.dirname(__file__))
require_clean_submodules(root_dir, sys.argv)

# Make sure javascript libraries are built
require_js_libs(root_dir, sys.argv)


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
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
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.6'],
      )
