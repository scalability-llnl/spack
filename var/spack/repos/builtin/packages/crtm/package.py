# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crtm(CMakePackage):
    """The Community Radiative Transfer Model (CRTM) package.
    The CRTM is composed of four important modules for gaseous transmittance,
    surface emission and reflection, cloud and aerosol absorption and
    scattering, and a solver for a radiative transfer."""

    homepage = "https://www.jcsda.org/jcsda-project-community-radiative-transfer-model"
    git = "https://github.com/JCSDA/crtm.git"
    url = "https://github.com/JCSDA/crtm/archive/refs/tags/v2.3.0.tar.gz"

    maintainers(
        "BenjaminTJohnson",
        "t-brown",
        "edwardhartnett",
        "AlexanderRichert-NOAA",
        "Hang-Lei-NOAA",
        "climbfuji",
    )

    variant(
        "fix", default=False, description='Download CRTM coeffecient or "fix" files (several GBs).'
    )

    depends_on("cmake@3.15:", type="build")
    depends_on("git-lfs")
    depends_on("netcdf-fortran", when="@2.4.0:")
    depends_on("netcdf-fortran", when="@v2.3-jedi.4")
    depends_on("netcdf-fortran", when="@v2.4-jedi.1")
    depends_on("netcdf-fortran", when="@v2.4-jedi.2")
    depends_on("netcdf-fortran", when="@v2.4.1-jedi")
    depends_on("netcdf-fortran", when="@v3")

    depends_on("crtm-fix@2.3.0_emc", when="@2.3.0 +fix")
    depends_on("crtm-fix@2.4.0_emc", when="@=2.4.0 +fix")
    depends_on("crtm-fix@2.4.0.1_emc", when="@2.4.0.1 +fix")

    depends_on("ecbuild", type=("build"), when="@v2.3-jedi.4")
    depends_on("ecbuild", type=("build"), when="@v2.4-jedi.1")
    depends_on("ecbuild", type=("build"), when="@v2.4-jedi.2")
    depends_on("ecbuild", type=("build"), when="@v2.4.1-jedi")
    depends_on("ecbuild", type=("build"), when="@v3.0")
    depends_on("ecbuild", type=("build"), when="@v3.1.0-skylabv7")

    license("CC0-1.0")

    version(
        "v3.1.0-skylabv8",
        sha256="a475c8a444072aef1e8c2babba3d12f13ab0fb6c7ecab88edad57130839e29ff",
    )
    version(
        "v3.1.0-skylabv7",
        sha256="3ac45c49562ab41c3baf443ce382e3a6bcb7226831b54146d9f73995be165ec7",
    )
    version(
        "v3.0.0-skylabv6",
        sha256="780fbc4e0f3b0414fbade4b595832bb35d9c5d3e7c3b25ad128ca94f71bea2b8",
    )
    version(
        "v3.0.0-skylabv5",
        sha256="4fa5dd2d65b4d4ff77d50992e8e0c02a59584b35599f424085fccdc2174d7bd2",
    )
    version(
        "v2.4.1-jedi", sha256="fd8bf4db4f2a3b420b4186de84483ba2a36660519dffcb1e0ff14bfe8c6f6a14"
    )
    version("v2.4-jedi.2", commit="62831cbb6c1ffcbb219eeec60e1b1c422526f597")
    version("v2.4-jedi.1", commit="82223419fdb479d76c2f2109c2b704e1d9618f22")
    version("2.4.0.1", tag="v2.4.0_emc.3", commit="7ecad4866c400d7d0db1413348ee225cfa99ff36")
    # REL-2.4.0_emc (v2.4.0 ecbuild does not work)
    version("2.4.0", commit="5ddd0d6b0138284764065feda73b5adf599082a2")
    # Uses the tip of REL-2.3.0_emc branch
    version("2.3.0", commit="99760e693ce3b90a3b3b0e97d80972b4dfb61196")

    depends_on("fortran", type="build")  # generated

    def url_for_version(self, version):
        if self.spec.satisfies("@v3") or version >= Version("3.0.0"):
            return f"https://github.com/JCSDA/crtmv3/archive/refs/tags/{version}.tar.gz"
        else:
            return f"https://github.com/JCSDA/crtm/archive/refs/tags/{version}.tar.gz"

    # https://github.com/JCSDA/spack-stack/issues/1088
    patch("v3.1.0-skylabv8.installprefix.patch", when="@v3.1.0-skylabv8")

    @when("@2.4.0.1")
    def patch(self):
        if self.compiler.name in ["gcc", "clang", "apple-clang"]:
            # Line lengths in RSS_Emissivity_Model.f90 are too long for gfortran default limit
            filter_file(
                "-fbacktrace", "-fbacktrace -ffree-line-length-none", "libsrc/CMakeLists.txt"
            )
