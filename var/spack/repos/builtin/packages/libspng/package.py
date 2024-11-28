# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libspng(CMakePackage):
    """libspng (simple png) is a C library for reading and writing
    Portable Network Graphics (PNG) format files with a focus on
    security and ease of use."""

    homepage = "https://github.com/randy408/libspng"
    url = "https://github.com/randy408/libspng/archive/refs/tags/v0.7.2.tar.gz"

    maintainers("sethrj")

    license("BSD-2-Clause")

    version("0.7.4", sha256="47ec02be6c0a6323044600a9221b049f63e1953faf816903e7383d4dc4234487")
    version("0.7.2", sha256="4acf25571d31f540d0b7ee004f5461d68158e0a13182505376805da99f4ccc4e")

    depends_on("c", type="build")
    depends_on("zlib")

    def cmake_args(self):
        target = self.spec.target
        return [
            self.define("BUILD_EXAMPLES", False),
            self.define("ENABLE_OPT", target.vendor != "generic"),
        ]
