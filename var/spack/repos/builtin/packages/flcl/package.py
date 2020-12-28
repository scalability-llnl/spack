# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Flcl(CMakePackage):
    """API for Fortran to C++ and C++ to Fortran multi-dimensional array
    interoperability using Kokkos."""

    homepage = "https://github.com/kokkos/kokkos-fortran-interop"
    git      = "https://github.com/kokkos/kokkos-fortran-interop.git"
    url      = "https://github.com/kokkos/kokkos-fortran-interop/releases/download/0.3/0.3.tar.gz"

    maintainers = ['womeld', 'agaspar']

    version('develop', branch='develop')
    version('0.3', sha256='0586b981b976588d8059e5bf1bf71fb5a7153ea950c7e2b562a3d812fefee56e')

    depends_on('kokkos')
    depends_on('cmake@3.17:', type='build')

    def cmake_args(self):
        args = []
        args.append('-DBUILD_TESTING:BOOL={0}'.format(
                    'ON' if self.run_tests else 'OFF'))

        return args
