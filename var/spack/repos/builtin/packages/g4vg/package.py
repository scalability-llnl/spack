# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class G4vg(CMakePackage):
    """Generate VecGeom geometry representations from in-memory Geant4 geometry.
    """

    homepage = "https://github.com/celeritas-project/g4vg"
    url = "https://github.com/celeritas-project/g4vg/releases/download/v1.0.1/g4vg-1.0.1.tar.gz"

    maintainers("sethrj", "drbenmorgan")

    license("Apache-2.0", checked_by="sethrj")

    version("1.0.1", sha256="add7ce4bc37889cac2101323a997cea8574b18da6cbeffdab44a2b714d134e99")

    variant("debug", default=False, description="Enable runtime debug assertions")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("cxx", type="build")
    depends_on("vecgeom@1.2.8:")
    depends_on("geant4")

    def cmake_args(self):
        define = self.define
        from_variant = self.define_from_variant
        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("G4VG_DEBUG", "debug"),
            define("G4VG_BUILD_TESTS", False),
        ]

        return args
