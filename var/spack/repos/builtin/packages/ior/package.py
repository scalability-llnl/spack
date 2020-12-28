# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ior(AutotoolsPackage):
    """The IOR software is used for benchmarking parallel file systems
    using POSIX, MPI-IO, or HDF5 interfaces."""

    homepage = "https://github.com/hpc/ior"
    url      = "https://github.com/hpc/ior/archive/3.2.1.tar.gz"

    version('develop', git='https://github.com/hpc/ior.git', branch='master')
    version('3.3.0rc1', sha256='0e42ebf5b5adae60625bf97989c8e2519d41ea2e3d18561d7d5b945625317aa5')
    version('3.2.1', sha256='ebcf2495aecb357370a91a2d5852cfd83bba72765e586bcfaf15fb79ca46d00e', preferred=True)
    version('3.2.0', sha256='91a766fb9c34b5780705d0997b71b236a1120da46652763ba11d9a8c44251852')
    version('3.0.1', sha256='0cbefbcdb02fb13ba364e102f9e7cc2dcf761698533dac25de446a3a3e81390d')

    variant('hdf5',  default=False, description='support IO with HDF5 backend')
    variant('ncmpi', default=False, description='support IO with NCMPI backend')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('mpi')
    depends_on('hdf5+mpi', when='+hdf5')
    depends_on('parallel-netcdf', when='+ncmpi')

    # The build for 3.2.0 fails if hdf5 is enabled
    # See https://github.com/hpc/ior/pull/124
    patch('https://github.com/hpc/ior/commit/1dbca5c293f95074f9887ddb2043fa984670fb4d.patch',
          sha256='f28d6638a74a09e147e9fa870930e54a82ff580d1c232add47a67c375e255ada',
          when='@3.2.0 +hdf5')

    @run_before('autoreconf')
    def bootstrap(self):
        Executable('./bootstrap')()

    def configure_args(self):
        spec = self.spec
        config_args = []

        env['CC'] = spec['mpi'].mpicc

        if '+hdf5' in spec:
            config_args.append('--with-hdf5')
            config_args.append('CFLAGS=-D H5_USE_16_API')
        else:
            config_args.append('--without-hdf5')

        if '+ncmpi' in spec:
            config_args.append('--with-ncmpi')
        else:
            config_args.append('--without-ncmpi')

        return config_args
