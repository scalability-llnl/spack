# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5py(PythonPackage):
    """The h5py package provides both a high- and low-level interface to the
    HDF5 library from Python."""

    homepage = "http://www.h5py.org/"
    url      = "https://pypi.io/packages/source/h/h5py/h5py-2.10.0.tar.gz"
    git      = "https://github.com/h5py/h5py.git"

    version('master', branch='master')
    version('2.10.0', sha256='84412798925dc870ffd7107f045d7659e60f5d46d1c70c700375248bf6bf512d')
    version('2.9.0', sha256='9d41ca62daf36d6b6515ab8765e4c8c4388ee18e2a665701fef2b41563821002')
    version('2.8.0', sha256='e626c65a8587921ebc7fb8d31a49addfdd0b9a9aa96315ea484c09803337b955')
    version('2.7.1', sha256='180a688311e826ff6ae6d3bda9b5c292b90b28787525ddfcb10a29d5ddcae2cc')
    version('2.7.0', sha256='79254312df2e6154c4928f5e3b22f7a2847b6e5ffb05ddc33e37b16e76d36310')
    version('2.6.0', sha256='b2afc35430d5e4c3435c996e4f4ea2aba1ea5610e2d2f46c9cae9f785e33c435')
    version('2.5.0', sha256='9833df8a679e108b561670b245bcf9f3a827b10ccb3a5fa1341523852cfac2f6')
    version('2.4.0', sha256='faaeadf4b8ca14c054b7568842e0d12690de7d5d68af4ecce5d7b8fc104d8e60')

    variant('mpi', default=True, description='Build with MPI support')

    # Build dependencies
    depends_on('py-cython@0.23:', type='build')
    depends_on('py-pkgconfig', type='build')
    depends_on('py-setuptools', type='build')

    # Build and runtime dependencies
    depends_on('py-cached-property@1.5:', type=('build', 'run'))
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Link dependencies
    depends_on('hdf5@1.8.4:+hl')

    # MPI dependencies
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))

    phases = ['configure', 'install']

    def configure(self, spec, prefix):
        self.setup_py('configure', '--hdf5={0}'.format(spec['hdf5'].prefix),
                      '--hdf5-version={0}'.format(spec['hdf5'].version))

        if '+mpi' in spec:
            env['CC'] = spec['mpi'].mpicc
            self.setup_py('configure', '--mpi')
