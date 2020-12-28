# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Spherepack(Package):
    """SPHEREPACK - A Package for Modeling Geophysical Processes"""

    homepage = "https://www2.cisl.ucar.edu/resources/legacy/spherepack"
    url      = "https://www2.cisl.ucar.edu/sites/default/files/spherepack3.2.tar"

    version('3.2', sha256='d58ef8cbc45cf2ad24f73a9f73f5f9d4fbe03cd9e2e7722e526fffb68be581ba')

    def install(self, spec, prefix):
        if self.compiler.fc is None:
            raise InstallError("SPHEREPACK requires a Fortran 90 compiler")
        make("MAKE=make", "F90=f90 -O2", "AR=ar", "libspherepack")
        make("MAKE=make", "F90=f90 -O2", "AR=ar", "testspherepack")
        install_tree("lib", prefix.lib)
