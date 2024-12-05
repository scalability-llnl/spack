# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gegelati(CMakePackage):
    """Class to add the a TPG library(gegelati) into Spack"""

    homepage = "https://github.com/gegelati/gegelati"
    url = "https://github.com/gegelati/gegelati/archive/refs/tags/v1.2.0.tar.gz"

    # notify when the package is updated.
    maintainers("lucascarvalhoroncoroni")

    license("CECILL-C")

    version("1.2.0", sha256="039997c7d6cb394f910f6c40620165b32094e0c85c170be01eb74b55488a1d4c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("sdl2")
    depends_on("doxygen")

    def cmake_args(self):
        args = []
        return args
