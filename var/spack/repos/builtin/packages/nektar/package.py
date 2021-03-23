# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Nektar(CMakePackage):
    """Nektar++: Spectral/hp Element Framework"""

    homepage = "https://www.nektar.info/"
    url      = "https://gitlab.nektar.info/nektar/nektar/-/archive/v4.4.1/nektar-v4.4.1.tar.bz2"

    version('5.0.0', sha256='5c594453fbfaa433f732a55405da9bba27d4a00c32d7b9d7515767925fb4a818')
    version('4.4.1', sha256='71cfd93d848a751ae9ae5e5ba336cee4b4827d4abcd56f6b8dc5c460ed6b738c')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('fftw', default=True, description='Builds with fftw support')
    variant('arpack', default=True, description='Builds with arpack support')
    variant('hdf5', default=True, description='Builds with hdf5 support')
    variant('scotch', default=False,
            description='Builds with scotch partitioning support')

    depends_on('cmake@2.8.8:', type='build', when="~hdf5")
    depends_on('cmake@3.2:', type='build', when="+hdf5")

    depends_on('blas')
    depends_on('lapack')
    depends_on('boost@1.56.0: +iostreams')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('tinyxml', when='platform=darwin')

    depends_on('mpi', when='+mpi')
    depends_on('fftw@3.0: +mpi', when="+mpi+fftw")
    depends_on('fftw@3.0: ~mpi', when="~mpi+fftw")
    depends_on('arpack-ng +mpi', when="+arpack+mpi")
    depends_on('arpack-ng ~mpi', when="+arpack~mpi")
    depends_on('hdf5 +mpi +hl', when="+mpi+hdf5")
    depends_on('scotch ~mpi ~metis', when="~mpi+scotch")
    depends_on('scotch +mpi ~metis', when="+mpi+scotch")

    conflicts("+hdf5", when="~mpi",
              msg="Nektar's hdf5 output is for parallel builds only")

    def cmake_args(self):
        args = []

        def hasfeature(feature):
            return 'ON' if feature in self.spec else 'OFF'

        args.append('-DNEKTAR_USE_MPI=%s' % hasfeature('+mpi'))
        args.append('-DNEKTAR_USE_FFTW=%s' % hasfeature('+fftw'))
        args.append('-DNEKTAR_USE_ARPACK=%s' % hasfeature('+arpack'))
        args.append('-DNEKTAR_USE_HDF5=%s' % hasfeature('+hdf5'))
        args.append('-DNEKTAR_USE_SCOTCH=%s' % hasfeature('+scotch'))
        args.append('-DNEKTAR_USE_PETSC=OFF')
        return args
