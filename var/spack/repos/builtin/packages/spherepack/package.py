# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Spherepack(Package):
    """SPHEREPACK - A Package for Modeling Geophysical Processes"""

    homepage = "https://github.com/NCAR/NCAR-Classic-Libraries-for-Geophysics"
    url = "https://github.com/NCAR/NCAR-Classic-Libraries-for-Geophysics/raw/refs/heads/main/SpherePack/spherepack3.2.tar.gz"

    version("3.2", sha256="7f5497e77101a4423cee887294f873048f6ff6bc8d0e908c8a89ece677ee19ea")

    depends_on("fortran", type="build")

    def install(self, spec, prefix):
        if self.compiler.fc is None:
            raise InstallError("SPHEREPACK requires a Fortran 90 compiler")
        make("MAKE=make", "F90=f90 -O2 -fallow-argument-mismatch", "AR=ar", "libspherepack")
        make("MAKE=make", "F90=f90 -O2 -fallow-argument-mismatch", "AR=ar", "testspherepack")
        install_tree("lib", prefix.lib)
