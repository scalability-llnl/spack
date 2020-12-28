# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTables(PythonPackage):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""

    homepage = "http://www.pytables.org/"
    url      = "https://pypi.io/packages/source/t/tables/tables-3.6.1.tar.gz"

    version('3.6.1', sha256='49a972b8a7c27a8a173aeb05f67acb45fe608b64cd8e9fa667c0962a60b71b49')
    version('3.6.0', sha256='db3488214864fb313a611fca68bf1c9019afe4e7877be54d0e61c84416603d4d')
    version('3.5.2', sha256='b220e32262bab320aa41d33125a7851ff898be97c0de30b456247508e2cc33c2')
    version('3.4.4', sha256='bdc5c073712af2a43babd139c4855fc99496bb2c3f3f5d1b4770a985e6f9ce29')
    version('3.3.0', sha256='8383ccf02e041a5d55494a09fc5514140b4653055a2732c981b5fd0f7408822c')
    version('3.2.2', sha256='3564b351a71ec1737b503b001eb7ceae1f65d5d6e3ffe1ea75aafba10f37fa84')

    variant('zlib', default=True, description='Support for zlib compression')
    variant('bzip2', default=False, description='Support for bzip2 compression')
    variant('lzo', default=False, description='Support for lzo compression')

    # requirements.txt
    depends_on('python@3.5:', when='@3.6.1:', type=('build', 'run'))
    depends_on('python@3.4:', when='@3.6.0:', type=('build', 'run'))
    depends_on('python@2.6:', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython@0.21:', type='build')
    depends_on('py-numpy@1.9.3:', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', when='@:3.5', type=('build', 'run'))
    # tables/req_versions.py
    depends_on('hdf5@1.8.4:1.8.999', when='@:3.3.99')
    depends_on('hdf5@1.8.4:', when='@3.4.0:')
    # Versions prior to 3.3 must build with the internal blosc due to a lock
    # problem in a multithreaded environment.
    depends_on('c-blosc@1.4.1:', when='@3.3.0:')
    depends_on('zlib', when='+zlib')
    depends_on('bzip2', when='+bzip2')
    depends_on('lzo', when='+lzo')

    def setup_build_environment(self, env):
        env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        if '+bzip2' in self.spec:
            env.set('BZIP2_DIR', self.spec['bzip2'].prefix)
        if '+lzo' in self.spec:
            env.set('LZO_DIR', self.spec['lzo'].prefix)
        if '^c-blosc' in self.spec:
            env.set('BLOSC_DIR', self.spec['c-blosc'].prefix)
