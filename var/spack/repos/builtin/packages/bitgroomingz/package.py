# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bitgroomingz(CMakePackage):
    """BGZ: Bit Grooming Compressor"""

    homepage = "https://github.com/disheng222/BitGroomingZ"
    git = "https://github.com/disheng222/BitGroomingZ"

    maintainers("robertu94")

    version("master", branch="master")
    version("2022-10-14", commit="a018b20cca9f7d6a5396ab36230e4be6ae1cb25b")

    depends_on("c", type="build")  # generated

    variant("shared", default=True, description="build shared libs")

    depends_on("zlib-api")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args
