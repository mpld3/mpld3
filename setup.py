from distutils.core import setup

DESCRIPTION = "D3 Viewer for Matplotlib"
LONG_DESCRIPTION = DESCRIPTION
NAME = "mpld3"
AUTHOR = "Jake VanderPlas"
AUTHOR_EMAIL = "jakevdp@cs.washington.edu"
MAINTAINER = "Jake VanderPlas"
MAINTAINER_EMAIL = "jakevdp@cs.washington.edu"
DOWNLOAD_URL = 'http://github.com/jakevdp/mpld3'
LICENSE = 'BSD 3-clause'

# partial import to get version
import mpld3
VERSION = mpld3.__version__

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=DOWNLOAD_URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=['mpld3']
     )
