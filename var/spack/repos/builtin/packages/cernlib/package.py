# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cernlib(CMakePackage):
    """CERN Library"""

    homepage = "https://cernlib.web.cern.ch"
    url = "https://cernlib.web.cern.ch/download/2023_source/tar/cernlib-2023.08.14.0-free.tar.gz"

    maintainers("andriish")
    version(
        "2022.11.08.0-free",
        sha256="733d148415ef78012ff81f21922d3bf641be7514b0242348dd0200cf1b003e46",
    )
    version(
        "2023.08.14.0-free",
        sha256="7006475d9c38254cb94ce75e556a319fea3b3155087780ea522003103771474e",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")

    depends_on("freetype")
    depends_on("motif")
    depends_on("libnsl")
    depends_on("libx11")
    depends_on("libxaw")
    depends_on("libxt")
    depends_on("libxcrypt")

    depends_on("xbae", when="@2023:")

    depends_on("openssl", when="platform=linux")

    def patch(self):
        if self.spec.satisfies("@:2023.08.14.0-free"):
            filter_file("crypto", "crypt", "packlib/CMakeLists.txt")
        if self.spec.satisfies("@2023.08.14.0-free"):
            filter_file(
                r"\${MOTIF_LIBRARIES} \${Xbae}", "${Xbae} ${MOTIF_LIBRARIES}", "CMakeLists.txt"
            )

    def cmake_args(self):
        args = [self.define_from_variant("CERNLIB_BUILD_SHARED", "shared")]
        return args
