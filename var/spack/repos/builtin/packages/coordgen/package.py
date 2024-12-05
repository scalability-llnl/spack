# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Coordgen(CMakePackage):
    """Schrödinger, Inc's 2D coordinate generation"""

    homepage = "https://github.com/schrodinger/coordgenlibs"
    url = "https://github.com/schrodinger/coordgenlibs/archive/refs/tags/v3.0.2.tar.gz"

    maintainers("RMeli")

    license("BSD-3-Clause")

    version("3.0.2", sha256="f67697434f7fec03bca150a6d84ea0e8409f6ec49d5aab43badc5833098ff4e3")

    depends_on("cxx", type="build")  # generated

    variant("maeparser", default=True, description="Use MAE parser")
    variant("example", default=False, description="Build sample executable")
    variant("shared", default=True, description="Build as shared library")

    depends_on("maeparser", when="+maeparser")
    depends_on("boost", when="+maeparser")

    def cmake_args(self):
        args = [
            self.define_from_variant("COORDGEN_BUILD_EXAMPLE", "example"),
            self.define_from_variant("COORDGEN_USE_MAEPARSER", "maeparser"),
            self.define_from_variant("COORDGEN_BUILD_SHARED_LIBS", "shared"),
        ]
        return args
