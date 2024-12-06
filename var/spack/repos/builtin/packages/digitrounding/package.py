# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Digitrounding(CMakePackage):
    """Standalone version of Digit rounding compressor"""

    homepage = "https://github.com/disheng222/digitroundingZ"
    git = "https://github.com/disheng222/digitroundingZ"

    maintainers("robertu94")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("2020-02-27", commit="7b18679aded7a85e6f221f7f5cd4f080f322bc33")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    variant("shared", default=True, description="build shared libraries")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args
