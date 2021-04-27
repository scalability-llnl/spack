# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Openmc(CMakePackage):
    """The OpenMC project aims to provide a fully-featured Monte Carlo particle
       transport code based on modern methods. It is a constructive solid
       geometry, continuous-energy transport code that uses ACE format cross
       sections. The project started under the Computational Reactor Physics
       Group at MIT."""

    homepage = "http://openmc.readthedocs.io/"
    url = "https://github.com/openmc-dev/openmc/tarball/v0.10.0"
    git = "https://github.com/openmc-dev/openmc.git"

    version('develop', branch='develop', submodules=True)
    version('master', branch='master', submodules=True)
    version('0.12.0', tag='v0.12.0', submodules=True)
    version('0.11.0', sha256='19a9d8e9c3b581e9060fbd96d30f1098312d217cb5c925eb6372a5786d9175af')
    version('0.10.0', sha256='47650cb45e2c326ae439208d6f137d75ad3e5c657055912d989592c6e216178f')

    variant('mpi', default=False, description='Enable MPI support')
    variant('openmp', default=True, description='Enable OpenMP support')
    variant('optimize', default=False, description='Enable optimization flags')
    variant('debug', default=False, description='Enable debug flags')

    depends_on('git', type='build')
    depends_on('hdf5+hl~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5+hl+mpi', when='+mpi')

    def cmake_args(self):
        options = ['-DCMAKE_INSTALL_LIBDIR=lib']  # forcing bc sometimes goes to lib64

        if '+mpi' in self.spec:
            options += ['-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc,
                        '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx]

        options += [self.define_from_variant('openmp')]
        options += [self.define_from_variant('optimize')]
        options += [self.define_from_variant('debug')]

        if '+optimize' in self.spec:
            self.spec.variants['build_type'].value = 'Release'

        if '+debug' in self.spec:
            self.spec.variants['build_type'].value = 'Debug'

        return options
