from spack import *

class PyNumpy(Package):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/numpy"
    url      = "https://pypi.python.org/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    version('1.9.1', '78842b73560ec378142665e712ae4ad9')

    extends('python')
    depends_on('py-nose')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
