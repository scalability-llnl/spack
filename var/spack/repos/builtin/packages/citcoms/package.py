# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Citcoms(AutotoolsPackage):
    """CitcomS is a finite element code designed to solve compressible
    thermochemical convection problems relevant to Earth's mantle."""

    homepage = "https://geodynamics.org/cig/software/citcoms/"
    url      = "https://github.com/geodynamics/citcoms/releases/download/v3.3.1/CitcomS-3.3.1.tar.gz"
    git      = "https://github.com/geodynamics/citcoms.git"

    maintainers = ['adamjstewart']

    version('master', branch='master', submodules=True)
    version('3.3.1', sha256='e3520e0a933e4699d31e86fe309b8c154ea6ecb0f42a1cf6f25e8d13d825a4b3')
    version('3.2.0', sha256='773a14d91ecbb4a4d1e04317635fab79819d83c57b47f19380ff30b9b19cb07a')

    variant('ggrd', default=False, description='use GGRD file support')
    variant('cuda', default=False, description='use CUDA')
    variant('hdf5', default=False, description='add HDF5 support')

    # Required dependencies
    depends_on('mpi')
    depends_on('zlib')
    depends_on('python@:2', type='run')  # needed for post-processing scripts
    depends_on('automake', when='@master', type='build')
    depends_on('autoconf', when='@master', type='build')
    depends_on('libtool',  when='@master', type='build')
    depends_on('m4',       when='@master', type='build')

    # Optional dependencies
    depends_on('hc', when='+ggrd')
    depends_on('cuda', when='+cuda')
    depends_on('hdf5+mpi', when='+hdf5')

    def setup_build_environment(self, env):
        if '+ggrd' in self.spec:
            env.set('HC_HOME', self.spec['hc'].prefix)

    def configure_args(self):
        args = ['CC={0}'.format(self.spec['mpi'].mpicc)]

        # Flags only valid in 3.2
        if self.spec.satisfies('@:3.2'):
            args.append('--without-pyre')
            args.append('--without-exchanger')

        if '+ggrd' in self.spec:
            args.append('--with-ggrd')
        else:
            args.append('--without-ggrd')

        if '+cuda' in self.spec:
            args.append('--with-cuda')
        else:
            args.append('--without-cuda')

        if '+hdf5' in self.spec:
            args.extend([
                '--with-hdf5',
                # https://github.com/geodynamics/citcoms/issues/2
                'CPPFLAGS=-DH5_USE_16_API',
                'CFLAGS=-DH5_USE_16_API'
            ])
        else:
            args.append('--without-hdf5')

        return args
