# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fortrilinos(CMakePackage):
    """ForTrilinos provides a set of Fortran-2003 wrappers to the Trilinos
    solver library.

    Note that most properties are *transitive* from the underlying Trilinos
    configuration. For example, MPI is enabled if and only if the linked
    Trilinos version has it, so this package does not provide an indepdent
    variant. Instead, use ``fortrilinos ^trilinos~mpi`` to disable MPI support.

    Since Trilinos enables a bunch of upstream dependencies by default, it
    might be worthwhile to disable them::

        spack install fortrilinos \
            ^trilinos@12.18.1+nox+stratimikos \
            ~boost~exodus~glm~gtest~hdf5~hypre~matio~metis~mumps~netcdf~suite-sparse
    """

    homepage = "https://trilinos.github.io/ForTrilinos/"
    url      = "https://github.com/trilinos/ForTrilinos/archive/v2.0.0.tar.gz"
    git      = "https://github.com/trilinos/ForTrilinos.git"

    maintainers = ['sethrj', 'aprokop']

    version('2.0.0', sha256='9af3b3eea9934e44d74654a5fa822de08bd0efa43e06e4a4e35a777781f542d6')
    # Note: spack version comparison implies Version('2.0.0') <
    # Version('2.0.0-dev1'), so this is the best workaround I could find.
    version('2.0.dev3',
            sha256='c20a34b374a56b050bc1db0be1d3db63fca3e59c5803af0cb851b044ac84e6b3',
            url="https://github.com/trilinos/ForTrilinos/archive/v2.0.0-dev3.tar.gz")
    version('2.0.dev2',
            sha256='2a55c668b3fe986583658d272eab2dc076b291a5f2eb582a02602db86a32030b',
            url="https://github.com/trilinos/ForTrilinos/archive/v2.0.0-dev2.tar.gz")
    version('2.0.dev1',
            sha256='ab664ce2d7fe75c524d7ff6b1efffa3e459ab5739a916e6ea810ae40f39ca4f4',
            url="https://github.com/trilinos/ForTrilinos/archive/v2.0.0-dev1.tar.gz")
    version('master', branch='master')

    variant('hl', default=True, description='Build high-level Trilinos wrappers')
    variant('shared', default=True, description='Build shared libraries')

    # Trilinos version dependencies
    depends_on('trilinos@13.0.0:', when='@2.0.0:')
    depends_on('trilinos@12.18.1', when='@2.0.dev3')
    depends_on('trilinos@12.18.1', when='@2.0.dev2')
    depends_on('trilinos@12.17.1', when='@2.0.dev1')

    # Baseline trilinos dependencies
    depends_on('trilinos+teuchos gotype=long_long')
    # Full trilinos dependencies
    depends_on('trilinos+amesos2+anasazi+belos+kokkos+ifpack2+muelu+nox+tpetra'
               '+stratimikos', when='+hl')

    @run_before('cmake')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies, require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError('ForTrilinos requires a Fortran compiler')

    def cmake_args(self):
        return [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('ForTrilinos_EXAMPLES', self.run_tests),
            self.define('ForTrilinos_TESTING', self.run_tests),
        ]
